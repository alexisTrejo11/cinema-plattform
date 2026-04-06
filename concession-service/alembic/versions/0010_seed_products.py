"""seed products

Revision ID: 0010
Revises: 0009
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0010"
down_revision: Union[str, Sequence[str], None] = "0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
INSERT INTO products (id, name, description, price, image_url, is_available, preparation_time_mins, calories, category_id) VALUES
('75bb2bef-953f-47b2-8e48-6f3101515ebe','Classic Popcorn (Large)', 'Our signature buttery popcorn - large size', 8.99, 'popcorn_classic_large.jpg', true, 2, 600, 1),
('be6eb059-dfbc-4f8e-b162-2f106a4f1426','Caramel Popcorn (Medium)', 'Sweet caramel coated popcorn', 6.99, 'popcorn_caramel_med.jpg', true, 2, 550, 1),
('59a4286f-80ae-44ce-8e4f-d0fe8c4dd09d','Cheese Popcorn (Small)', 'Savory cheese flavored popcorn', 4.99, 'popcorn_cheese_small.jpg', true, 2, 450, 1),
('4f699451-3666-46bc-bcce-6d410c763744', 'Twin Pack Popcorn', 'Two medium popcorns - one classic, one caramel', 10.99, 'popcorn_twinpack.jpg', true, 3, 1100, 1),
('50e16df9-7bec-451e-965b-7bbff6aa4be4', 'Large Soda', '32oz fountain drink - choice of flavor', 5.99, 'soda_large.jpg', true, 1, 300, 2),
('34348831-f2b7-41ae-810c-97c5d73a6724', 'Bottled Water', 'Premium spring water 500ml', 3.50, 'water_bottle.jpg', true, 1, 0, 2),
('ddca49df-ff11-4626-b394-bd6517c160eb', 'Iced Tea (Medium)', 'Fresh brewed iced tea', 4.50, 'icedtea_med.jpg', true, 1, 120, 2),
('4ee01845-ec47-483b-8347-f3024afd5a60', 'slushie_large', 'Slushie (Large)', 5.25, 'slushie_large.jpg', true, 1, 250, 2),
('b0bbe6fa-518a-4f73-ab89-84884235b513', 'M&M''s (Large)', 'Milk chocolate candies 200g', 4.75, 'mms_large.jpg', true, 1, 500, 3),
('4647a046-5ecf-4ec3-a497-75521a08e800', 'Sour Patch Kids', 'Tangy sugar-coated candy 150g', 4.25, 'sourpatch.jpg', true, 1, 400, 3),
('db0945ad-2013-4c42-817c-fb00fdaac87f', 'Chocolate Bar', 'Premium milk chocolate 100g', 3.99, 'chocolate_bar.jpg', true, 1, 550, 3),
('6cbfb414-4740-451b-9f4f-2e62e27a25f5', 'Gummy Bears', 'Fruit flavored gummies 120g', 3.75, 'gummy_bears.jpg', true, 1, 350, 3),
('53c78d5a-9a17-42aa-bf9f-04c42a88a189' ,'Hot Dog', 'Classic beef hot dog with toppings', 6.50, 'hotdog.jpg', true, 5, 450, 4),
('c52d2f1b-6acd-420b-9fba-8acfdc80f0ad', 'Nachos with Cheese', 'Crispy tortilla chips with melted cheese', 7.25, 'nachos.jpg', true, 4, 600, 4),
('914a5106-ac8f-43db-b482-99792e11c92e', 'Chicken Tenders (3pc)', 'Crispy chicken tenders with dipping sauce', 8.99, 'chicken_tenders.jpg', true, 6, 700, 4),
('29285e7b-bb75-473c-96d3-e6f7a7bffb00', 'Pretzel with Cheese', 'Soft pretzel with cheese dip', 5.75, 'pretzel.jpg', true, 3, 500, 4)
ON CONFLICT (id) DO NOTHING
"""
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
DELETE FROM products WHERE id IN (
    '75bb2bef-953f-47b2-8e48-6f3101515ebe',
    'be6eb059-dfbc-4f8e-b162-2f106a4f1426',
    '59a4286f-80ae-44ce-8e4f-d0fe8c4dd09d',
    '4f699451-3666-46bc-bcce-6d410c763744',
    '50e16df9-7bec-451e-965b-7bbff6aa4be4',
    '34348831-f2b7-41ae-810c-97c5d73a6724',
    'ddca49df-ff11-4626-b394-bd6517c160eb',
    '4ee01845-ec47-483b-8347-f3024afd5a60',
    'b0bbe6fa-518a-4f73-ab89-84884235b513',
    '4647a046-5ecf-4ec3-a497-75521a08e800',
    'db0945ad-2013-4c42-817c-fb00fdaac87f',
    '6cbfb414-4740-451b-9f4f-2e62e27a25f5',
    '53c78d5a-9a17-42aa-bf9f-04c42a88a189',
    'c52d2f1b-6acd-420b-9fba-8acfdc80f0ad',
    '914a5106-ac8f-43db-b482-99792e11c92e',
    '29285e7b-bb75-473c-96d3-e6f7a7bffb00'
)
"""
        )
    )
