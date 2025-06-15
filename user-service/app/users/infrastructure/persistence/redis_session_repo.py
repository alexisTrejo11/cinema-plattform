import json
from datetime import datetime, timezone
from app.auth.application.repositories import SessionRepository
from typing import Any, Dict, Optional, List
from app.auth.domain.entities import SessionToken
from redis import Redis 

class RedisSessionRepository(SessionRepository):
    def __init__(self, redis_conn: Redis) -> None:
        self.redis_conn = redis_conn
        super().__init__()

    async def create(self, token: SessionToken) -> None:
        key = self._generate_key(str(token.user_id), token.token)
        
        # Convert SessionToken to dictionary
        session_dict = token.__dict__.copy()
        if isinstance(session_dict.get('expires_at'), datetime):
            session_dict['expires_at'] = session_dict['expires_at'].isoformat()
        if isinstance(session_dict.get('created_at'), datetime):
            session_dict['created_at'] = session_dict['created_at'].isoformat()
        
        # Use regular Redis SET with JSON serialization
        self.redis_conn.set(key, json.dumps(session_dict))
        
        # Set expiration based on expires_at
        if token.expires_at:
            expires_in_seconds = int((token.expires_at - datetime.now()).total_seconds())
            if expires_in_seconds > 0:
                self.redis_conn.expire(key, expires_in_seconds)
    
    async def get_user_token(self, user_id: str, token: str) -> Optional[SessionToken]:
        key = self._generate_key(user_id, token)
        session_data_json = self.redis_conn.get(key)
        
        if not session_data_json:
            return None
            
        try:
            session_data = json.loads(session_data_json)
            return self._dict_to_session_token(session_data)
        except (json.JSONDecodeError, KeyError):
            return None

    async def list_by_user_id(self, user_id: str) -> List[SessionToken]:
        pattern = f"session:{user_id}:*"
        keys = self.redis_conn.keys(pattern)
        sessions: List[SessionToken] = []
        
        if not keys:
            return sessions
        
        # Use pipeline for efficiency
        pipe = self.redis_conn.pipeline()
        for key in keys:
            pipe.get(key)
        
        results = pipe.execute()
        
        for result in results:
            if result:
                try:
                    session_data = json.loads(result)
                    session_token = self._dict_to_session_token(session_data)
                    if session_token:
                        sessions.append(session_token)
                except (json.JSONDecodeError, KeyError):
                    continue
        
        return sessions

    async def revoke_user_token(self, user_id: str, token: str) -> bool:
        key = self._generate_key(user_id, token)
        session_data_json = self.redis_conn.get(key)
        
        if not session_data_json:
            return False
            
        try:
            session_data = json.loads(session_data_json)
            session_data['is_revoked'] = True
            self.redis_conn.set(key, json.dumps(session_data))
            return True
        except (json.JSONDecodeError, KeyError):
            return False

    async def revoke_all_user_tokens(self, user_id: str) -> bool:
        pattern = f"session:{user_id}:*"
        keys = self.redis_conn.keys(pattern)
    
        if not keys:
            return False
        
        # Use pipeline for efficiency
        pipe = self.redis_conn.pipeline()
        
        # First, get all session data
        for key in keys:
            pipe.get(key)
        
        results = pipe.execute()
        
        # Then update all sessions
        pipe = self.redis_conn.pipeline()
        updated_count = 0
        
        for i, result in enumerate(results):
            if result:
                try:
                    session_data = json.loads(result)
                    session_data['is_revoked'] = True
                    pipe.set(keys[i], json.dumps(session_data))
                    updated_count += 1
                except (json.JSONDecodeError, KeyError):
                    continue
        
        if updated_count > 0:
            pipe.execute()
            return True
        
        return False

    async def cleanup_expired_tokens(self) -> int:
        """Mark expired tokens as revoked instead of deleting them"""
        count = 0
        current_time = datetime.now()
        
        cursor = 0
        while True:
            cursor, keys = self.redis_conn.scan(
                cursor=cursor,
                match='session:*:*',
                count=1000
            )
            
            if not keys:
                if cursor == 0:
                    break
                continue
            
            # Get all session data
            pipe = self.redis_conn.pipeline()
            for key in keys:
                pipe.get(key)
            
            results = pipe.execute()
            
            # Update expired sessions
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
                                    update_pipe.set(keys[i], json.dumps(session_data))
                                    count += 1
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
            
            if count > 0:
                update_pipe.execute()
            
            if cursor == 0:
                break
        
        return count
    
    def _generate_key(self, user_id: str, token_id: Optional[str] = None) -> str:
        if token_id:
            return f"session:{user_id}:{token_id}"
        return f"session:{user_id}"
    
    def _dict_to_session_token(self, session_data: Dict[str, Any]) -> Optional[SessionToken]:
        """Convert dictionary to SessionToken object"""
        try:
            expires_at = session_data.get('expires_at')
            if expires_at and isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            
            created_at = session_data.get('created_at')
            if created_at and isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
            
            return SessionToken(
                user_id=session_data['user_id'],
                token=session_data['token'],
                expires_at=expires_at,
                is_revoked=session_data.get('is_revoked', False),
                created_at=created_at
            )
        except KeyError:
            return None