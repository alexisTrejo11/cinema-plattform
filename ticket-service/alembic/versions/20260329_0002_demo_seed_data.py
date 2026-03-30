"""Insert demo ticket and seat rows for local development.

Revision ID: 20260329_0002
Revises: 20260329_0001
Create Date: 2026-03-29

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260329_0002"
down_revision: Union[str, Sequence[str], None] = "20260329_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO tickets (user_id, movie_id, showtime_id, transaction_id, price, status)
        VALUES
            (1, 101, 501, 'txn-demo-001', 12.50, 'CONFIRMED'),
            (2, 102, 501, 'txn-demo-002', 15.00, 'CONFIRMED'),
            (NULL, 101, 502, 'txn-demo-003', 9.99, 'PENDING')
        """
    )
    op.execute(
        """
        INSERT INTO showtime_seats (showtime_id, ticket_id, seat_row, seat_number, seat_type)
        SELECT 501, t.id, 'A', 1, 'STANDARD'
        FROM tickets t WHERE t.transaction_id = 'txn-demo-001'
        UNION ALL
        SELECT 501, t.id, 'A', 2, 'STANDARD'
        FROM tickets t WHERE t.transaction_id = 'txn-demo-002'
        UNION ALL
        SELECT 502, NULL, 'B', 5, 'VIP'
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM showtime_seats
        WHERE showtime_id IN (501, 502)
           OR ticket_id IN (SELECT id FROM tickets WHERE transaction_id LIKE 'txn-demo-%')
        """
    )
    op.execute(
        """
        DELETE FROM tickets WHERE transaction_id LIKE 'txn-demo-%'
        """
    )
