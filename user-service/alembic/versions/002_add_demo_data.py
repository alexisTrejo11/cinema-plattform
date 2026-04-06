"""Insert demo users for local development.

Revision ID: 002_add_demo_data
Revises: 001_create_user_tables
Create Date: 2025-03-23

Demo accounts use bcrypt hash of the password "password" (development only).
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002_add_demo_data"
down_revision: Union[str, Sequence[str], None] = "001_create_user_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# bcrypt ("password") — for non-production demo rows only
_DEMO_PASSWORD_HASH = (
    "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31mW"
)

_DEMO_EMAILS = (
    "demo.customer@cinema.local",
    "demo.admin@cinema.local",
)


def upgrade() -> None:
    op.execute(
        f"""
        INSERT INTO users (
            email,
            password,
            phone_number,
            first_name,
            last_name,
            role,
            gender,
            is_2fa_enabled,
            status,
            date_of_birth
        ) VALUES
        (
            '{_DEMO_EMAILS[0]}',
            '{_DEMO_PASSWORD_HASH}',
            '+10000000001',
            'Demo',
            'Customer',
            'CUSTOMER'::role_enum,
            'OTHER'::gender_enum,
            false,
            'ACTIVE'::user_status_enum,
            '1990-06-15 00:00:00'
        ),
        (
            '{_DEMO_EMAILS[1]}',
            '{_DEMO_PASSWORD_HASH}',
            '+10000000002',
            'Demo',
            'Admin',
            'ADMIN'::role_enum,
            'OTHER'::gender_enum,
            false,
            'ACTIVE'::user_status_enum,
            '1985-03-20 00:00:00'
        );
        """
    )


def downgrade() -> None:
    emails = "', '".join(_DEMO_EMAILS)
    op.execute(f"DELETE FROM users WHERE email IN ('{emails}');")
