import json
from typing import Any, Dict, Optional, List
from datetime import datetime, date
from enum import Enum
from redis import Redis
from app.token.domain.token import Token, TokenType
from app.token.application.repository import TokenRepository
import logging

logger = logging.getLogger(__name__)

def json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    logger.debug(f"json_serializer encountered unhandled type: {type(obj)} with value: {obj}")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

class TokenRepositoryImpl(TokenRepository):
    def __init__(self, redis_conn: Redis) -> None:
        self.redis_conn = redis_conn
        super().__init__()

    def _generate_key(self, user_id: str, token_code: str, token_type: TokenType) -> str:
        """Generates a unique key for the Redis entry, including token type."""
        return f"session:{user_id}:{token_type.value}:{token_code}"

    def _dict_to_jwt_token(self, session_data: Dict[str, Any]) -> Optional[Token]:
        """Convert dictionary to Token object."""
        try:
            expires_at = session_data.get('expires_at')
            if expires_at and isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)

            created_at = session_data.get('created_at')
            if created_at and isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
                
            token_type_str = session_data.get('type')
            token_type = None
            if token_type_str:
                try:
                    token_type = TokenType(token_type_str)
                except ValueError:
                    logger.warning(f"Invalid TokenType value '{token_type_str}' in session data for user_id: {session_data.get('user_id')}. Returning None.")
                    return None

            return Token(
                user_id=session_data['user_id'],
                code=session_data['code'],
                expires_at=expires_at,
                is_revoked=session_data.get('is_revoked', False),
                type=token_type,
                created_at=created_at
            )
        except (KeyError, TypeError, ValueError) as e:
            logger.error(f"Error converting dict to Token: {e} - Data: {session_data}")
            return None

    def create(self, token: Token) -> None:
        key = self._generate_key(str(token.user_id), token.code, token.type)

        expires_in_seconds = 0
        if token.expires_at:
            time_difference = token.expires_at - datetime.now()
            expires_in_seconds = int(time_difference.total_seconds())

        # Synchronous call
        self.redis_conn.set(key, json.dumps(token.__dict__, default=json_serializer))

        if expires_in_seconds > 0:
            # Synchronous call
            self.redis_conn.expire(key, expires_in_seconds)
        else:
            logger.warning(f"Token for user {token.user_id} expires in the past or is non-expiring. Not setting expiration.")

    def get_user_token(self, user_id: str, token_code: str, token_type: TokenType) -> Optional[Token]:
        key = self._generate_key(user_id, token_code, token_type)
        session_data_json = self.redis_conn.get(key)

        if not session_data_json:
            return None

        try:
            session_data = json.loads(session_data_json)
            return self._dict_to_jwt_token(session_data)
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(f"Error loading or parsing session data for key {key}: {e}")
            return None

    def list_by_user_id(self, user_id: str, token_type: Optional[TokenType] = None) -> List[Token]:
        pattern = f"session:{user_id}:{token_type.value if token_type else '*'}:*"
        
        all_keys = []
        cursor = 0
        while True:
            # Synchronous scan
            cursor, keys = self.redis_conn.scan(
                cursor=cursor,
                match=pattern,
                count=1000
            )
            all_keys.extend(keys)
            if cursor == 0:
                break

        if not all_keys:
            return []

        pipe = self.redis_conn.pipeline()
        for key in all_keys:
            pipe.get(key)
        
        results = pipe.execute() # Synchronous execute

        sessions: List[Token] = []
        for result in results:
            if result:
                try:
                    session_data = json.loads(result)
                    session_token = self._dict_to_jwt_token(session_data)
                    if session_token:
                        sessions.append(session_token)
                except (json.JSONDecodeError, KeyError, AttributeError):
                    continue
        
        return sessions

    def revoke_user_token(self, user_id: str, token_code: str, token_type: TokenType) -> bool:
        key = self._generate_key(user_id, token_code, token_type)
        session_data_json = self.redis_conn.get(key) # Synchronous call

        if not session_data_json:
            return False
            
        try:
            session_data = json.loads(session_data_json)
            
            is_revoked: bool = session_data['is_revoked']
            if is_revoked and is_revoked:
                logger.error(f"{key}: already revoked")
                return False
            
            
            session_data['is_revoked'] = True
            self.redis_conn.set(key, json.dumps(session_data, default=json_serializer)) # Synchronous call
            return True
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(f"Error revoking token for key {key}: {e}")
            return False

    def revoke_all_user_tokens(self, user_id: str, token_type: Optional[TokenType] = None) -> bool:
        pattern = f"session:{user_id}:{token_type.value if token_type else '*'}:*"
        
        all_keys = []
        cursor = 0
        while True:
            cursor, keys = self.redis_conn.scan( # Synchronous scan
                cursor=cursor,
                match=pattern,
                count=1000
            )
            all_keys.extend(keys)
            if cursor == 0:
                break

        if not all_keys:
            return False
        
        pipe = self.redis_conn.pipeline()
        for key in all_keys:
            pipe.get(key)
        
        results = pipe.execute() # Synchronous execute

        update_pipe = self.redis_conn.pipeline()
        updated_count = 0
        
        for i, result in enumerate(results):
            if result:
                try:
                    session_data = json.loads(result)
                    if not session_data.get('is_revoked', False):
                        session_data['is_revoked'] = True
                        update_pipe.set(all_keys[i], json.dumps(session_data, default=json_serializer))
                        updated_count += 1
                except (json.JSONDecodeError, KeyError, AttributeError):
                    continue
        
        if updated_count > 0:
            update_pipe.execute() # Synchronous execute
            return True
        
        return False

    def cleanup_expired_tokens(self) -> int:
        """Mark expired tokens as revoked instead of deleting them."""
        count = 0
        current_time = datetime.now()
        cursor = 0
        while True:
            cursor, keys = self.redis_conn.scan( # Synchronous scan
                cursor=cursor,
                match='session:*:*:*',
                count=1000
            )
            
            if not keys:
                if cursor == 0:
                    break
                continue
            
            pipe = self.redis_conn.pipeline()
            for key in keys:
                pipe.get(key)
            
            results = pipe.execute() # Synchronous execute
            
            update_pipe = self.redis_conn.pipeline()
            
            for i, result in enumerate(results):
                if result:
                    try:
                        session_data = json.loads(result)
                        if not session_data.get('is_revoked', False):
                            expires_at_str = session_data.get('expires_at')
                            if expires_at_str:
                                expires_at = datetime.fromisoformat(expires_at_str)

                                if expires_at < current_time:
                                    session_data['is_revoked'] = True
                                    update_pipe.set(keys[i], json.dumps(session_data, default=json_serializer))
                                    count += 1
                    except (json.JSONDecodeError, KeyError, ValueError, AttributeError) as e:
                        logger.error(f"Error processing session data for cleanup for key {keys[i]}: {e}. Data: {result}")
                        continue
            
            if update_pipe:
                update_pipe.execute() # Synchronous execute
            
            if cursor == 0:
                break
        
        return count