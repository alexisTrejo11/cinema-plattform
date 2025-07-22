-- Insert food categories
INSERT INTO product_categories (name, description, is_active) VALUES
('Popcorn', 'Freshly popped cinema popcorn varieties', true),
('Drinks', 'Cold beverages and refreshments', true),
('Candy', 'Assorted chocolates and sweets', true),
('Hot Food', 'Hot snacks and meals', true),
('Combo Meals', 'Special value meal deals', true);

-- Insert popcorn products
INSERT INTO products (id, name, description, price, image_url, is_available, preparation_time_mins, calories, category_id) VALUES
('75bb2bef-953f-47b2-8e48-6f3101515ebe','Classic Popcorn (Large)', 'Our signature buttery popcorn - large size', 8.99, 'popcorn_classic_large.jpg', true, 2, 600, 1),
('be6eb059-dfbc-4f8e-b162-2f106a4f1426','Caramel Popcorn (Medium)', 'Sweet caramel coated popcorn', 6.99, 'popcorn_caramel_med.jpg', true, 2, 550, 1),
('59a4286f-80ae-44ce-8e4f-d0fe8c4dd09d','Cheese Popcorn (Small)', 'Savory cheese flavored popcorn', 4.99, 'popcorn_cheese_small.jpg', true, 2, 450, 1),
('4f699451-3666-46bc-bcce-6d410c763744', 'Twin Pack Popcorn', 'Two medium popcorns - one classic, one caramel', 10.99, 'popcorn_twinpack.jpg', true, 3, 1100, 1);

-- Insert drink products
INSERT INTO products (name, description, price, image_url, is_available, preparation_time_mins, calories, category_id) VALUES
('Large Soda', '32oz fountain drink - choice of flavor', 5.99, 'soda_large.jpg', true, 1, 300, 2),
('Bottled Water', 'Premium spring water 500ml', 3.50, 'water_bottle.jpg', true, 1, 0, 2),
('Iced Tea (Medium)', 'Fresh brewed iced tea', 4.50, 'icedtea_med.jpg', true, 1, 120, 2),
('Slushie (Large)', 'Ice-cold flavored slush', 5.25, 'slushie_large.jpg', true, 1, 250, 2);

-- Insert candy products
INSERT INTO products (name, description, price, image_url, is_available, preparation_time_mins, calories, category_id) VALUES
('M&M''s (Large)', 'Milk chocolate candies 200g', 4.75, 'mms_large.jpg', true, 1, 500, 3),
('Sour Patch Kids', 'Tangy sugar-coated candy 150g', 4.25, 'sourpatch.jpg', true, 1, 400, 3),
('Chocolate Bar', 'Premium milk chocolate 100g', 3.99, 'chocolate_bar.jpg', true, 1, 550, 3),
('Gummy Bears', 'Fruit flavored gummies 120g', 3.75, 'gummy_bears.jpg', true, 1, 350, 3);

-- Insert hot food products
INSERT INTO products (name, description, price, image_url, is_available, preparation_time_mins, calories, category_id) VALUES
('Hot Dog', 'Classic beef hot dog with toppings', 6.50, 'hotdog.jpg', true, 5, 450, 4),
('Nachos with Cheese', 'Crispy tortilla chips with melted cheese', 7.25, 'nachos.jpg', true, 4, 600, 4),
('Chicken Tenders (3pc)', 'Crispy chicken tenders with dipping sauce', 8.99, 'chicken_tenders.jpg', true, 6, 700, 4),
('Pretzel with Cheese', 'Soft pretzel with cheese dip', 5.75, 'pretzel.jpg', true, 3, 500, 4);

-- Insert combos
INSERT INTO combos (name, description, price, discount_percentage, image_url, is_available) VALUES
('Classic Movie Night', 'Large popcorn + large soda + candy choice', 15.99, 15, 'combo_classic.jpg', true),
('Sweet Lovers Duo', 'Caramel popcorn + slushie + chocolate bar', 13.50, 10, 'combo_sweet.jpg', true),
('Savory Snack Pack', 'Cheese popcorn + hot dog + medium soda', 16.75, 12, 'combo_savory.jpg', true),
('Family Bundle', '2 large popcorns + 4 medium drinks + 2 candies', 32.99, 20, 'combo_family.jpg', true),
('Ultimate Feast', 'Large popcorn + nachos + chicken tenders + 2 large drinks', 28.50, 18, 'combo_ultimate.jpg', true);


-- Insert combo items for Classic Movie Night (combo_id 1)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
(1, 1, 1),  -- Large classic popcorn
(1, 5, 1),  -- Large soda
(1, 9, 1);  -- M&M's

-- Insert combo items for Sweet Lovers Duo (combo_id 2)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
(2, 2, 1),  -- Caramel popcorn
(2, 8, 1),  -- Slushie
(2, 11, 1); -- Chocolate bar

-- Insert combo items for Savory Snack Pack (combo_id 3)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
(3, 3, 1),  -- Cheese popcorn
(3, 13, 1), -- Hot dog
(3, 5, 1);  -- Medium soda (using large soda product with quantity adjustment)

-- Insert combo items for Family Bundle (combo_id 4)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
(4, 1, 2),  -- 2 large popcorns
(4, 5, 4),  -- 4 medium drinks (using large soda product)
(4, 9, 1),  -- M&M's
(4, 10, 1); -- Sour Patch Kids

-- Insert combo items for Ultimate Feast (combo_id 5)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
(5, 1, 1),  -- Large popcorn
(5, 14, 1), -- Nachos
(5, 15, 1), -- Chicken tenders
(5, 5, 2);  -- 2 large drinks