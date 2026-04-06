"""Create user enums and users table.

Revision ID: 001_create_user_tables
Revises:
Create Date: 2025-03-23

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001_create_user_tables"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE TYPE gender_enum AS ENUM ('MALE', 'FEMALE', 'OTHER')"
    )
    op.execute(
        "CREATE TYPE role_enum AS ENUM ('CUSTOMER', 'EMPLOYEE', 'MANAGER', 'ADMIN')"
    )
    op.execute(
        "CREATE TYPE user_status_enum AS ENUM ('PENDING', 'ACTIVE', 'INACTIVE', 'BANNED')"
    )
    op.execute(
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255),
            phone_number VARCHAR(20) UNIQUE,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            role role_enum NOT NULL,
            gender gender_enum NOT NULL,
            is_2fa_enabled BOOLEAN DEFAULT false,
            totp_secret VARCHAR(255),
            status user_status_enum NOT NULL DEFAULT 'PENDING',
            date_of_birth TIMESTAMP NOT NULL,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS users")
    op.execute("DROP TYPE IF EXISTS user_status_enum")
    op.execute("DROP TYPE IF EXISTS role_enum")
    op.execute("DROP TYPE IF EXISTS gender_enum")
