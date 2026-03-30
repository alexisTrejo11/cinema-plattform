"""Create tickets and showtime_seats tables.

Revision ID: 20260329_0001
Revises:
Create Date: 2026-03-29

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260329_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE tickets(
            id SERIAL PRIMARY KEY,
            user_id integer,
            movie_id integer NOT NULL,
            showtime_id integer NOT NULL,
            transaction_id VARCHAR(255) NOT NULL,
            price NUMERIC(10,2) CONSTRAINT positive_price CHECK (price > 0),
            status VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    op.execute(
        """
        CREATE TABLE showtime_seats(
            id SERIAL PRIMARY KEY,
            showtime_id integer NOT NULL,
            ticket_id integer,
            seat_row VARCHAR(10),
            seat_number integer,
            seat_type VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(showtime_id, seat_row, seat_number),
            FOREIGN KEY(ticket_id) REFERENCES tickets(id)
        )
        """
    )
    op.execute(
        "CREATE INDEX showtime_seat_row_number_idx ON showtime_seats(showtime_id, seat_row, seat_number)"
    )
    op.execute("CREATE INDEX tickets_user_id_idx ON tickets(user_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS showtime_seat_row_number_idx")
    op.execute("DROP INDEX IF EXISTS tickets_user_id_idx")
    op.execute("DROP TABLE IF EXISTS showtime_seats")
    op.execute("DROP TABLE IF EXISTS tickets")
