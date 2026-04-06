"""create catalog schema

Revision ID: 0001_create_catalog_schema
Revises:
Create Date: 2026-04-03 00:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_catalog_schema"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


cinema_type_enum = sa.Enum("VIP", "TRADITIONAL", name="cinema_type_enum")
cinema_status_enum = sa.Enum("OPEN", "CLOSED", "MAINTENANCE", name="cinema_status_enum")
location_region_enum = sa.Enum(
    "CDMX_SOUTH",
    "CDMX_NORTH",
    "CDMX_CENTER",
    "CDMX_EAST",
    "CDMX_WEST",
    name="location_region_enum",
)
movie_genre_enum = sa.Enum(
    "ACTION",
    "COMEDY",
    "DRAMA",
    "ROMANCE",
    "THRILLER",
    "SCI_FI",
    name="movie_genre",
)
movie_rating_enum = sa.Enum("G", "PG", "PG_13", "R", "NC_17", name="movie_rating")
theater_type_enum = sa.Enum("TWO_D", "THREE_D", "IMAX", "FOUR_DX", "VIP", name="theater_type_enum")
seat_type_enum = sa.Enum(
    "STANDARD",
    "VIP",
    "FOUR_DX",
    "ACCESSIBLE",
    "PREMIUM",
    "LOVESEAT",
    name="seat_type_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    cinema_type_enum.create(bind, checkfirst=True)
    cinema_status_enum.create(bind, checkfirst=True)
    location_region_enum.create(bind, checkfirst=True)
    movie_genre_enum.create(bind, checkfirst=True)
    movie_rating_enum.create(bind, checkfirst=True)
    theater_type_enum.create(bind, checkfirst=True)
    seat_type_enum.create(bind, checkfirst=True)

    op.create_table(
        "cinemas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("image", sa.Text(), nullable=False, server_default=""),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("tax_number", sa.String(255), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("screens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_renovation", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("type", cinema_type_enum, nullable=False),
        sa.Column("status", cinema_status_enum, nullable=False),
        sa.Column("region", location_region_enum, nullable=False),
        sa.Column("has_parking", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("has_food_court", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("has_coffee_station", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("has_disabled_access", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("address", sa.String(500), nullable=False),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("email_contact", sa.String(255), nullable=False, unique=True),
        sa.Column("latitude", sa.Float(precision=53), nullable=False),
        sa.Column("longitude", sa.Float(precision=53), nullable=False),
        sa.Column("facebook_url", sa.Text(), nullable=True),
        sa.Column("instagram_url", sa.Text(), nullable=True),
        sa.Column("x_url", sa.Text(), nullable=True),
        sa.Column("tik_tok_url", sa.Text(), nullable=True),
        sa.Column("features", sa.ARRAY(sa.String()), nullable=False, server_default="{}"),
    )

    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("original_title", sa.String(200), nullable=True),
        sa.Column("minute_duration", sa.Integer(), nullable=False),
        sa.Column("release_date", sa.Date(), nullable=False),
        sa.Column("synopsis", sa.String(), nullable=False),
        sa.Column("genre", movie_genre_enum, nullable=False),
        sa.Column("rating", movie_rating_enum, nullable=False),
        sa.Column("poster_url", sa.String(), nullable=True),
        sa.Column("trailer_url", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("projection_start_date", sa.Date(), nullable=False),
        sa.Column("projection_end_date", sa.Date(), nullable=False),
    )

    op.create_table(
        "theaters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cinema_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("theater_type", theater_type_enum, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("maintenance_mode", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["cinema_id"], ["cinemas.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "theater_seats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("theater_id", sa.Integer(), nullable=False),
        sa.Column("seat_row", sa.String(5), nullable=False),
        sa.Column("seat_number", sa.Integer(), nullable=False),
        sa.Column("seat_type", seat_type_enum, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["theater_id"], ["theaters.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("theater_id", "seat_row", "seat_number", name="uq_theater_seat_position"),
    )


def downgrade() -> None:
    op.drop_table("theater_seats")
    op.drop_table("theaters")
    op.drop_table("movies")
    op.drop_table("cinemas")

    bind = op.get_bind()
    seat_type_enum.drop(bind, checkfirst=True)
    theater_type_enum.drop(bind, checkfirst=True)
    movie_rating_enum.drop(bind, checkfirst=True)
    movie_genre_enum.drop(bind, checkfirst=True)
    location_region_enum.drop(bind, checkfirst=True)
    cinema_status_enum.drop(bind, checkfirst=True)
    cinema_type_enum.drop(bind, checkfirst=True)
