"""seed demo payment_methods and sample payments (idempotent)

Revision ID: 20260331_03
Revises: 20260331_02
Create Date: 2026-03-31 12:30:00.000000

Uses fixed UUID primary keys and ON CONFLICT DO NOTHING so re-running
``alembic upgrade head`` does not duplicate rows.
"""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260331_03"
down_revision: Union[str, None] = "20260331_02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Stable UTC timestamps for reproducible demo data (naive, typical PG storage).
_DEMO_TS = datetime(2026, 3, 31, 12, 0, 0)


def upgrade() -> None:
    conn = op.get_bind()

    catalog_rows = [
        {
            "id": "11111111-1111-1111-1111-111111111101",
            "name": "Credit or debit card",
            "provider": "stripe",
            "type": "card",
            "stripe_code": "card",
            "is_active": True,
            "min_amount": Decimal("0.00"),
            "created_at": _DEMO_TS,
            "updated_at": _DEMO_TS,
            "deleted_at": None,
        },
        {
            "id": "11111111-1111-1111-1111-111111111102",
            "name": "Pay at Oxxo",
            "provider": "stripe",
            "type": "cash",
            "stripe_code": "oxxo",
            "is_active": True,
            "min_amount": Decimal("1.00"),
            "created_at": _DEMO_TS,
            "updated_at": _DEMO_TS,
            "deleted_at": None,
        },
        {
            "id": "11111111-1111-1111-1111-111111111103",
            "name": "Internal wallet",
            "provider": "internal",
            "type": "wallet",
            "stripe_code": "wallet",
            "is_active": True,
            "min_amount": Decimal("0.00"),
            "created_at": _DEMO_TS,
            "updated_at": _DEMO_TS,
            "deleted_at": None,
        },
    ]

    for row in catalog_rows:
        conn.execute(
            sa.text(
                """
                INSERT INTO payment_methods (
                    id, name, provider, type, stripe_code, is_active,
                    min_amount, created_at, updated_at, deleted_at
                ) VALUES (
                    :id, :name, :provider, :type, :stripe_code, :is_active,
                    :min_amount, :created_at, :updated_at, :deleted_at
                )
                ON CONFLICT (id) DO NOTHING
                """
            ),
            row,
        )

    payment_rows = [
        {
            "id": "22222222-2222-2222-2222-222222222201",
            "user_id": "33333333-3333-3333-3333-333333333301",
            "amount": Decimal("24.50"),
            "currency": "USD",
            "refunded_amount": Decimal("0.00"),
            "payment_method": "stripe",
            "payment_type": "ticket_purchase",
            "status": "pending",
            "created_at": _DEMO_TS,
            "updated_at": _DEMO_TS,
            "deleted_at": None,
            "expires_at": _DEMO_TS,
            "completed_at": None,
            "refunded_at": None,
            "external_reference": None,
            "stripe_payment_intent_id": "pi_demo_pending_001",
            "metadata": json.dumps(
                {"show_id": "demo-show-1", "showtime_id": "demo-st-1"}
            ),
            "failure_reason": None,
            "refund_reasons": json.dumps([]),
        },
        {
            "id": "22222222-2222-2222-2222-222222222202",
            "user_id": "33333333-3333-3333-3333-333333333301",
            "amount": Decimal("12.00"),
            "currency": "USD",
            "refunded_amount": Decimal("0.00"),
            "payment_method": "stripe",
            "payment_type": "food_purchase",
            "status": "completed",
            "created_at": _DEMO_TS,
            "updated_at": _DEMO_TS,
            "deleted_at": None,
            "expires_at": None,
            "completed_at": _DEMO_TS,
            "refunded_at": None,
            "external_reference": "stripe:ch_demo_001",
            "stripe_payment_intent_id": "pi_demo_completed_001",
            "metadata": json.dumps({"order_id": "demo-order-1"}),
            "failure_reason": None,
            "refund_reasons": json.dumps([]),
        },
    ]

    for p in payment_rows:
        conn.execute(
            sa.text(
                """
                INSERT INTO payments (
                    id, user_id, amount, currency, refunded_amount,
                    payment_method, payment_type, status,
                    created_at, updated_at, deleted_at,
                    expires_at, completed_at, refunded_at,
                    external_reference, stripe_payment_intent_id,
                    metadata, failure_reason, refund_reasons
                ) VALUES (
                    :id, :user_id, :amount, :currency, :refunded_amount,
                    :payment_method, :payment_type, :status,
                    :created_at, :updated_at, :deleted_at,
                    :expires_at, :completed_at, :refunded_at,
                    :external_reference, :stripe_payment_intent_id,
                    CAST(:metadata AS json), :failure_reason, CAST(:refund_reasons AS json)
                )
                ON CONFLICT (id) DO NOTHING
                """
            ),
            p,
        )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "DELETE FROM payments WHERE id IN ("
            "'22222222-2222-2222-2222-222222222201', "
            "'22222222-2222-2222-2222-222222222202')"
        )
    )
    conn.execute(
        sa.text(
            "DELETE FROM payment_methods WHERE id IN ("
            "'11111111-1111-1111-1111-111111111101', "
            "'11111111-1111-1111-1111-111111111102', "
            "'11111111-1111-1111-1111-111111111103')"
        )
    )
