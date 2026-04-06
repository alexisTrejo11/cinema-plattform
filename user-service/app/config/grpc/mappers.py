from datetime import datetime, timezone

from google.protobuf.timestamp_pb2 import Timestamp

from app.users.domain import Gender, Status, User, UserRole
from app.grpc.generated import users_pb2


def _datetime_to_proto(dt: datetime) -> Timestamp:
    ts = Timestamp()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    ts.FromDatetime(dt)
    return ts


_ROLE_TO_PROTO = {
    UserRole.ADMIN: users_pb2.USER_ROLE_ADMIN,
    UserRole.CUSTOMER: users_pb2.USER_ROLE_CUSTOMER,
    UserRole.EMPLOYEE: users_pb2.USER_ROLE_EMPLOYEE,
    UserRole.MANAGER: users_pb2.USER_ROLE_MANAGER,
}

_GENDER_TO_PROTO = {
    Gender.MALE: users_pb2.USER_GENDER_MALE,
    Gender.FEMALE: users_pb2.USER_GENDER_FEMALE,
    Gender.OTHER: users_pb2.USER_GENDER_OTHER,
}

_STATUS_TO_PROTO = {
    Status.PENDING: users_pb2.USER_STATUS_PENDING,
    Status.ACTIVE: users_pb2.USER_STATUS_ACTIVE,
    Status.INACTIVE: users_pb2.USER_STATUS_INACTIVE,
    Status.BANNED: users_pb2.USER_STATUS_BANNED,
}


def user_to_proto(user: User) -> users_pb2.UserResponse:
    last = user.last_name if user.last_name is not None else ""
    phone = user.phone_number if user.phone_number is not None else ""
    dob = user.date_of_birth.isoformat() if user.date_of_birth is not None else ""

    msg = users_pb2.UserResponse(
        id=user.id,
        email=str(user.email),
        first_name=user.first_name,
        last_name=last,
        gender=_GENDER_TO_PROTO.get(user.gender, users_pb2.USER_GENDER_UNSPECIFIED),
        date_of_birth=dob,
        phone_number=phone,
        role=_ROLE_TO_PROTO.get(user.role, users_pb2.USER_ROLE_UNSPECIFIED),
        status=_STATUS_TO_PROTO.get(user.status, users_pb2.USER_STATUS_UNSPECIFIED),
        is_2fa_enabled=user.is_2fa_enabled,
    )
    msg.created_at.CopyFrom(_datetime_to_proto(user.created_at))
    msg.updated_at.CopyFrom(_datetime_to_proto(user.updated_at))
    return msg
