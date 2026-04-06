"""Seed demo data: users, wallets, and sample transactions

Revision ID: 0002
Revises:     0001
Create Date: 2026-03-24

Inserts deterministic demo records with fixed UUIDs so that the downgrade
can delete them precisely without touching any real production data.

UUIDs are embedded as string literals — not as bound parameters — so that
the offline SQL generation (`alembic upgrade head --sql`) produces a valid,
copy-pasteable script with no NULL placeholders.

Demo accounts
─────────────
  admin@cinema.com     ADMIN                – no wallet (admins manage the platform)
  manager@cinema.com   MANAGER + EMPLOYEE   – wallet with 500.00 USD
  customer@cinema.com  CUSTOMER             – wallet with 125.00 USD

Transactions
────────────
  manager  wallet : +500.00 USD  add_credit  (initial top-up via bank_transfer)
  customer wallet : +200.00 USD  add_credit  (top-up via card)
  customer wallet :  -75.00 USD  buy_product (movie ticket — net balance 125.00 USD)
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# ── Revision identifiers ──────────────────────────────────────────────────────
revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ── Fixed UUIDs ───────────────────────────────────────────────────────────────
# Embedded as literals so offline SQL generation emits real values.

_USER_ADMIN_ID    = "11111111-1111-1111-1111-111111111111"
_USER_MANAGER_ID  = "22222222-2222-2222-2222-222222222222"
_USER_CUSTOMER_ID = "33333333-3333-3333-3333-333333333333"

_WALLET_MANAGER_ID  = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
_WALLET_CUSTOMER_ID = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"

_TXN_MANAGER_TOPUP_ID   = "cccccccc-cccc-cccc-cccc-cccccccccccc"
_TXN_CUSTOMER_TOPUP_ID  = "dddddddd-dddd-dddd-dddd-dddddddddddd"
_TXN_CUSTOMER_BUY_ID    = "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"

# Fake external payment-gateway reference IDs
_PAY_REF_MANAGER  = "f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1"
_PAY_REF_TOPUP    = "f2f2f2f2-f2f2-f2f2-f2f2-f2f2f2f2f2f2"
_PAY_REF_BUY      = "f3f3f3f3-f3f3-f3f3-f3f3-f3f3f3f3f3f3"


# ─────────────────────────────────────────────────────────────────────────────
# UPGRADE
# ─────────────────────────────────────────────────────────────────────────────

def upgrade() -> None:
    conn = op.get_bind()

    # ── 1. Demo users ─────────────────────────────────────────────────────────
    conn.execute(sa.text(f"""
        INSERT INTO users (id, email, roles, is_active, created_at)
        VALUES
          ('{_USER_ADMIN_ID}',
           'admin@cinema.com',
           ARRAY['ADMIN']::user_role_enum[],
           TRUE,
           NOW() AT TIME ZONE 'UTC'),

          ('{_USER_MANAGER_ID}',
           'manager@cinema.com',
           ARRAY['MANAGER', 'EMPLOYEE']::user_role_enum[],
           TRUE,
           NOW() AT TIME ZONE 'UTC'),

          ('{_USER_CUSTOMER_ID}',
           'customer@cinema.com',
           ARRAY['CUSTOMER']::user_role_enum[],
           TRUE,
           NOW() AT TIME ZONE 'UTC')
        ON CONFLICT (id) DO NOTHING
    """))

    # ── 2. Demo wallets ───────────────────────────────────────────────────────
    conn.execute(sa.text(f"""
        INSERT INTO cinema_wallets
            (id, user_id, balance_amount, balance_currency, created_at, updated_at)
        VALUES
          ('{_WALLET_MANAGER_ID}',
           '{_USER_MANAGER_ID}',
           500.00, 'USD',
           NOW() AT TIME ZONE 'UTC', NOW() AT TIME ZONE 'UTC'),

          ('{_WALLET_CUSTOMER_ID}',
           '{_USER_CUSTOMER_ID}',
           125.00, 'USD',
           NOW() AT TIME ZONE 'UTC', NOW() AT TIME ZONE 'UTC')
        ON CONFLICT (id) DO NOTHING
    """))

    # ── 3. Demo transactions ──────────────────────────────────────────────────
    # manager: single top-up of 500 USD
    # customer: top-up of 200 USD, then 75 USD movie purchase (net = 125 USD)
    conn.execute(sa.text(f"""
        INSERT INTO wallet_transactions
            (transaction_id, wallet_id, amount_value, amount_currency,
             transaction_type, payment_method, payment_reference, timestamp)
        VALUES
          -- manager wallet: initial credit via bank_transfer
          ('{_TXN_MANAGER_TOPUP_ID}',
           '{_WALLET_MANAGER_ID}',
           500.00, 'USD',
           'add_credit', 'bank_transfer', '{_PAY_REF_MANAGER}',
           NOW() AT TIME ZONE 'UTC'),

          -- customer wallet: top-up via card
          ('{_TXN_CUSTOMER_TOPUP_ID}',
           '{_WALLET_CUSTOMER_ID}',
           200.00, 'USD',
           'add_credit', 'card', '{_PAY_REF_TOPUP}',
           NOW() AT TIME ZONE 'UTC'),

          -- customer wallet: movie ticket purchase (75 USD deducted)
          ('{_TXN_CUSTOMER_BUY_ID}',
           '{_WALLET_CUSTOMER_ID}',
           75.00, 'USD',
           'buy_product', 'wallet', '{_PAY_REF_BUY}',
           NOW() AT TIME ZONE 'UTC')
        ON CONFLICT (transaction_id) DO NOTHING
    """))


# ─────────────────────────────────────────────────────────────────────────────
# DOWNGRADE  (removes exactly the rows inserted above — safe on any DB state)
# ─────────────────────────────────────────────────────────────────────────────

def downgrade() -> None:
    conn = op.get_bind()

    # Delete in child-first order to respect FK constraints
    conn.execute(sa.text(f"""
        DELETE FROM wallet_transactions
        WHERE transaction_id IN (
            '{_TXN_MANAGER_TOPUP_ID}',
            '{_TXN_CUSTOMER_TOPUP_ID}',
            '{_TXN_CUSTOMER_BUY_ID}'
        )
    """))

    conn.execute(sa.text(f"""
        DELETE FROM cinema_wallets
        WHERE id IN ('{_WALLET_MANAGER_ID}', '{_WALLET_CUSTOMER_ID}')
    """))

    conn.execute(sa.text(f"""
        DELETE FROM users
        WHERE id IN (
            '{_USER_ADMIN_ID}',
            '{_USER_MANAGER_ID}',
            '{_USER_CUSTOMER_ID}'
        )
    """))
