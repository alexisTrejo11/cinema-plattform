import grpc
from grpc import aio

from app.grpc.generated import users_pb2, users_pb2_grpc
from app.grpc.mappers import user_to_proto
from app.users.infrastructure.persistence.sqlalch_user_repo import SQLAlchemyUserRepository
from config.postgres_config import AsyncSessionLocal


class UsersGrpcServicer(users_pb2_grpc.UsersServiceServicer):
    async def GetUserById(self, request: users_pb2.GetUserByIdRequest, context: aio.ServicerContext):
        if request.id <= 0:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "id must be a positive integer")
        async with AsyncSessionLocal() as session:
            repo = SQLAlchemyUserRepository(session)
            user = await repo.get_by_id(int(request.id))
            if not user:
                return users_pb2.GetUserResponse(success=False, message="User not found")
            return users_pb2.GetUserResponse(success=True, user=user_to_proto(user))

    async def GetUserByEmail(self, request: users_pb2.GetUserByEmailRequest, context: aio.ServicerContext):
        email = (request.email or "").strip()
        if not email:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "email is required")
        async with AsyncSessionLocal() as session:
            repo = SQLAlchemyUserRepository(session)
            user = await repo.get_by_email(email)
            if not user:
                return users_pb2.GetUserResponse(success=False, message="User not found")
            return users_pb2.GetUserResponse(success=True, user=user_to_proto(user))

    async def GetUserByPhone(self, request: users_pb2.GetUserByPhoneRequest, context: aio.ServicerContext):
        phone = (request.phone or "").strip()
        if not phone:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "phone is required")
        async with AsyncSessionLocal() as session:
            repo = SQLAlchemyUserRepository(session)
            user = await repo.get_by_phone(phone)
            if not user:
                return users_pb2.GetUserResponse(success=False, message="User not found")
            return users_pb2.GetUserResponse(success=True, user=user_to_proto(user))
