"""Create initial schema: enums, users, cinema_wallets, wallet_transactions

Revision ID: 0001
Revises:     None  (first migration)
Create Date: 2026-03-24

Based on db/postgres/V1__create_user_table.sql  and
         db/postgres/V1__create_wallet_tables.sql

Notable detail:
  • transaction_type_enum uses LOWERCASE values ('add_credit', …) to match
    the Python TransactionType enum declared in
    app/wallet/domain/enums.py.
  • user_role_enum and currency_enum use UPPERCASE values, matching their
    respective Python enums.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# ── Revision identifiers ──────────────────────────────────────────────────────
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ── Enum helpers ──────────────────────────────────────────────────────────────
# Declared with create_type=False so Alembic won't auto-create them when they're
# referenced inside op.create_table(); we create them explicitly with op.execute().

user_role_enum = postgresql.ENUM(
    "ADMIN", "MANAGER", "EMPLOYEE", "CUSTOMER",
    name="user_role_enum",
    create_type=False,
)

currency_enum = postgresql.ENUM(
    "MXN", "USD", "EUR",
    name="currency_enum",
    create_type=False,
)

transaction_type_enum = postgresql.ENUM(
    "add_credit", "buy_product", "refund", "transfer_in", "transfer_out",
    name="transaction_type_enum",
    create_type=False,
)


# ─────────────────────────────────────────────────────────────────────────────
# UPGRADE
# ─────────────────────────────────────────────────────────────────────────────

def upgrade() -> None:
    # ── 1. Custom ENUM types ─────────────────────────────────────────────────
    op.execute(
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role_enum') THEN
                CREATE TYPE user_role_enum
                    AS ENUM ('ADMIN', 'MANAGER', 'EMPLOYEE', 'CUSTOMER');
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'currency_enum') THEN
                CREATE TYPE currency_enum
                    AS ENUM ('MXN', 'USD', 'EUR');
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'transaction_type_enum') THEN
                CREATE TYPE transaction_type_enum
                    AS ENUM ('add_credit', 'buy_product', 'refund',
                             'transfer_in', 'transfer_out');
            END IF;
        END $$;
        """
    )

    # ── 2. users ─────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column(
            "roles",
            postgresql.ARRAY(user_role_enum),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("(NOW() AT TIME ZONE 'UTC')"),
        ),
        # updated_at is set by application-level onupdate; nullable in the model
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )

    op.create_index("idx_users_email",           "users", ["email"],      unique=True)
    op.create_index("idx_users_is_active",        "users", ["is_active"])
    op.create_index(
        "idx_users_roles", "users", ["roles"],
        postgresql_using="gin",
    )
    op.create_index(
        "idx_users_active_created_at", "users",
        ["is_active", sa.text("created_at DESC")],
    )
    op.create_index("idx_users_deleted_at", "users", ["deleted_at"])

    # ── 3. cinema_wallets ─────────────────────────────────────────────────────
    op.create_table(
        "cinema_wallets",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            # index created explicitly below as idx_cinema_wallets_user_id
        ),
        sa.Column(
            "balance_amount",
            sa.Numeric(10, 2),
            nullable=False,
            server_default=sa.text("0.00"),
        ),
        sa.Column(
            "balance_currency",
            currency_enum,
            nullable=False,
            server_default=sa.text("'USD'"),
        ),
        # created_at / updated_at exist in the SQL schema; the SQLAlchemy model
        # does not currently map them (tech debt), but keeping them in the DB
        # preserves auditability and forward-compatibility.
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("(NOW() AT TIME ZONE 'UTC')"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("(NOW() AT TIME ZONE 'UTC')"),
        ),
    )

    op.create_index("idx_cinema_wallets_user_id", "cinema_wallets", ["user_id"])

    # ── 4. wallet_transactions ────────────────────────────────────────────────
    op.create_table(
        "wallet_transactions",
        sa.Column(
            "transaction_id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "wallet_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("cinema_wallets.id", ondelete="CASCADE"),
            nullable=False,
            # index created explicitly below as idx_wallet_transactions_wallet_id
        ),
        sa.Column("amount_value",    sa.Numeric(10, 2), nullable=False),
        sa.Column("amount_currency", currency_enum,     nullable=False),
        sa.Column("transaction_type", transaction_type_enum, nullable=False),
        sa.Column("payment_method",   sa.String(255),  nullable=False),
        sa.Column("payment_reference", sa.String(255), nullable=True),
        sa.Column(
            "timestamp",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("(NOW() AT TIME ZONE 'UTC')"),
        ),
    )

    op.create_index(
        "idx_wallet_transactions_wallet_id",
        "wallet_transactions", ["wallet_id"],
    )
    op.create_index(
        "idx_wallet_transactions_type",
        "wallet_transactions", ["transaction_type"],
    )
    op.create_index(
        "idx_wallet_transactions_timestamp",
        "wallet_transactions", [sa.text("timestamp DESC")],
    )
    op.create_index(
        "idx_wallet_transactions_wallet_id_timestamp",
        "wallet_transactions", ["wallet_id", sa.text("timestamp DESC")],
    )
    op.create_index(
        "idx_wallet_transactions_currency",
        "wallet_transactions", ["amount_currency"],
    )


# ─────────────────────────────────────────────────────────────────────────────
# DOWNGRADE  (full rollback — drops tables then types in dependency order)
# ─────────────────────────────────────────────────────────────────────────────

def downgrade() -> None:
    # ── 1. Drop tables (child → parent to respect FK constraints) ────────────
    op.drop_table("wallet_transactions")
    op.drop_table("cinema_wallets")
    op.drop_table("users")

    # ── 2. Drop custom ENUM types ─────────────────────────────────────────────
    op.execute("DROP TYPE IF EXISTS transaction_type_enum")
    op.execute("DROP TYPE IF EXISTS currency_enum")
    op.execute("DROP TYPE IF EXISTS user_role_enum")
