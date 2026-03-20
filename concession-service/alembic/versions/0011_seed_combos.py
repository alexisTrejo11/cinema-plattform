"""seed combos and combo items

Revision ID: 0011
Revises: 0010
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0011"
down_revision: Union[str, Sequence[str], None] = "0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
INSERT INTO combos (id, name, description, price, discount_percentage, image_url, is_available) VALUES
('ffc6ca2b-fac1-46cd-97e0-49a899b74d73', 'Classic Movie Night', 'Large popcorn + large soda + candy choice', 15.99, 15, 'combo_classic.jpg', true),
('0955ad3f-7bf5-47b0-ac46-230e747f34e5', 'Sweet Lovers Duo', 'Caramel popcorn + slushie + chocolate bar', 13.50, 10, 'combo_sweet.jpg', true),
('aa61b3c1-5497-4cb2-987c-7a39979b5e12', 'Savory Snack Pack', 'Cheese popcorn + hot dog + medium soda', 16.75, 12, 'combo_savory.jpg', true),
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', 'Family Bundle', '2 large popcorns + 4 medium drinks + 2 candies', 32.99, 20, 'combo_family.jpg', true),
('09330d25-b67f-4438-b615-b9d21e2bdc5f', 'Ultimate Feast', 'Large popcorn + nachos + chicken tenders + 2 large drinks', 28.50, 18, 'combo_ultimate.jpg', true)
ON CONFLICT (id) DO NOTHING
"""
        )
    )
    op.execute(
        sa.text(
            """
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
('ffc6ca2b-fac1-46cd-97e0-49a899b74d73', '75bb2bef-953f-47b2-8e48-6f3101515ebe', 1),
('ffc6ca2b-fac1-46cd-97e0-49a899b74d73', '50e16df9-7bec-451e-965b-7bbff6aa4be4', 1),
('ffc6ca2b-fac1-46cd-97e0-49a899b74d73', 'b0bbe6fa-518a-4f73-ab89-84884235b513', 1),
('0955ad3f-7bf5-47b0-ac46-230e747f34e5', 'be6eb059-dfbc-4f8e-b162-2f106a4f1426', 1),
('0955ad3f-7bf5-47b0-ac46-230e747f34e5', '4ee01845-ec47-483b-8347-f3024afd5a60', 1),
('0955ad3f-7bf5-47b0-ac46-230e747f34e5', 'db0945ad-2013-4c42-817c-fb00fdaac87f', 1),
('aa61b3c1-5497-4cb2-987c-7a39979b5e12', '59a4286f-80ae-44ce-8e4f-d0fe8c4dd09d', 1),
('aa61b3c1-5497-4cb2-987c-7a39979b5e12', '53c78d5a-9a17-42aa-bf9f-04c42a88a189', 1),
('aa61b3c1-5497-4cb2-987c-7a39979b5e12', '50e16df9-7bec-451e-965b-7bbff6aa4be4', 1),
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', '75bb2bef-953f-47b2-8e48-6f3101515ebe', 2),
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', '50e16df9-7bec-451e-965b-7bbff6aa4be4', 4),
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', 'b0bbe6fa-518a-4f73-ab89-84884235b513', 1),
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', '4647a046-5ecf-4ec3-a497-75521a08e800', 1),
('09330d25-b67f-4438-b615-b9d21e2bdc5f', '75bb2bef-953f-47b2-8e48-6f3101515ebe', 1),
('09330d25-b67f-4438-b615-b9d21e2bdc5f', 'c52d2f1b-6acd-420b-9fba-8acfdc80f0ad', 1),
('09330d25-b67f-4438-b615-b9d21e2bdc5f', '914a5106-ac8f-43db-b482-99792e11c92e', 1),
('09330d25-b67f-4438-b615-b9d21e2bdc5f', '50e16df9-7bec-451e-965b-7bbff6aa4be4', 2)
ON CONFLICT (combo_id, product_id) DO NOTHING
"""
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
DELETE FROM combo_items WHERE combo_id IN (
    'ffc6ca2b-fac1-46cd-97e0-49a899b74d73',
    '0955ad3f-7bf5-47b0-ac46-230e747f34e5',
    'aa61b3c1-5497-4cb2-987c-7a39979b5e12',
    '6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e',
    '09330d25-b67f-4438-b615-b9d21e2bdc5f'
)
"""
        )
    )
    op.execute(
        sa.text(
            """
DELETE FROM combos WHERE id IN (
    'ffc6ca2b-fac1-46cd-97e0-49a899b74d73',
    '0955ad3f-7bf5-47b0-ac46-230e747f34e5',
    'aa61b3c1-5497-4cb2-987c-7a39979b5e12',
    '6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e',
    '09330d25-b67f-4438-b615-b9d21e2bdc5f'
)
"""
        )
    )
