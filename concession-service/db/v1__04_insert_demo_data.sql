-- Insert categories
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
INSERT INTO products (id, name, description, price, image_url, is_available, preparation_time_mins, calories, category_id) VALUES
('50e16df9-7bec-451e-965b-7bbff6aa4be4', 'Large Soda', '32oz fountain drink - choice of flavor', 5.99, 'soda_large.jpg', true, 1, 300, 2),
('34348831-f2b7-41ae-810c-97c5d73a6724', 'Bottled Water', 'Premium spring water 500ml', 3.50, 'water_bottle.jpg', true, 1, 0, 2),
('ddca49df-ff11-4626-b394-bd6517c160eb', 'Iced Tea (Medium)', 'Fresh brewed iced tea', 4.50, 'icedtea_med.jpg', true, 1, 120, 2),
('4ee01845-ec47-483b-8347-f3024afd5a60', 'slushie_large', 'Slushie (Large)', 5.25, 'slushie_large.jpg', true, 1, 250, 2);

-- Insert candy products
INSERT INTO products (id, name, description, price, image_url, is_available, preparation_time_mins, calories, category_id) VALUES
('b0bbe6fa-518a-4f73-ab89-84884235b513', 'M&M''s (Large)', 'Milk chocolate candies 200g', 4.75, 'mms_large.jpg', true, 1, 500, 3),
('4647a046-5ecf-4ec3-a497-75521a08e800', 'Sour Patch Kids', 'Tangy sugar-coated candy 150g', 4.25, 'sourpatch.jpg', true, 1, 400, 3),
('db0945ad-2013-4c42-817c-fb00fdaac87f', 'Chocolate Bar', 'Premium milk chocolate 100g', 3.99, 'chocolate_bar.jpg', true, 1, 550, 3),
('6cbfb414-4740-451b-9f4f-2e62e27a25f5', 'Gummy Bears', 'Fruit flavored gummies 120g', 3.75, 'gummy_bears.jpg', true, 1, 350, 3);

-- Insert hot food products
INSERT INTO products (id, name, description, price, image_url, is_available, preparation_time_mins, calories, category_id) VALUES
('53c78d5a-9a17-42aa-bf9f-04c42a88a189' ,'Hot Dog', 'Classic beef hot dog with toppings', 6.50, 'hotdog.jpg', true, 5, 450, 4),
('c52d2f1b-6acd-420b-9fba-8acfdc80f0ad', 'Nachos with Cheese', 'Crispy tortilla chips with melted cheese', 7.25, 'nachos.jpg', true, 4, 600, 4),
('914a5106-ac8f-43db-b482-99792e11c92e', 'Chicken Tenders (3pc)', 'Crispy chicken tenders with dipping sauce', 8.99, 'chicken_tenders.jpg', true, 6, 700, 4),
('29285e7b-bb75-473c-96d3-e6f7a7bffb00', 'Pretzel with Cheese', 'Soft pretzel with cheese dip', 5.75, 'pretzel.jpg', true, 3, 500, 4);

-- Insert combos
INSERT INTO combos (id, name, description, price, discount_percentage, image_url, is_available) VALUES
('ffc6ca2b-fac1-46cd-97e0-49a899b74d73', 'Classic Movie Night', 'Large popcorn + large soda + candy choice', 15.99, 15, 'combo_classic.jpg', true),
('0955ad3f-7bf5-47b0-ac46-230e747f34e5', 'Sweet Lovers Duo', 'Caramel popcorn + slushie + chocolate bar', 13.50, 10, 'combo_sweet.jpg', true),
('aa61b3c1-5497-4cb2-987c-7a39979b5e12', 'Savory Snack Pack', 'Cheese popcorn + hot dog + medium soda', 16.75, 12, 'combo_savory.jpg', true),
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', 'Family Bundle', '2 large popcorns + 4 medium drinks + 2 candies', 32.99, 20, 'combo_family.jpg', true),
('09330d25-b67f-4438-b615-b9d21e2bdc5f', 'Ultimate Feast', 'Large popcorn + nachos + chicken tenders + 2 large drinks', 28.50, 18, 'combo_ultimate.jpg', true);


-- Insert combo items for Classic Movie Night (combo_id 1)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
('ffc6ca2b-fac1-46cd-97e0-49a899b74d73', '75bb2bef-953f-47b2-8e48-6f3101515ebe', 1),  -- Large classic popcorn
('ffc6ca2b-fac1-46cd-97e0-49a899b74d73', '50e16df9-7bec-451e-965b-7bbff6aa4be4', 1),  -- Large soda
('ffc6ca2b-fac1-46cd-97e0-49a899b74d73', 'b0bbe6fa-518a-4f73-ab89-84884235b513', 1);  -- M&M's

-- Insert combo items for Sweet Lovers Duo (combo_id 2)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
('0955ad3f-7bf5-47b0-ac46-230e747f34e5', 'be6eb059-dfbc-4f8e-b162-2f106a4f1426', 1),  -- Caramel popcorn
('0955ad3f-7bf5-47b0-ac46-230e747f34e5', '4ee01845-ec47-483b-8347-f3024afd5a60', 1),  -- Slushie
('0955ad3f-7bf5-47b0-ac46-230e747f34e5', 'db0945ad-2013-4c42-817c-fb00fdaac87f', 1); -- Chocolate bar

-- Insert combo items for Savory Snack Pack (combo_id 3)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
('aa61b3c1-5497-4cb2-987c-7a39979b5e12', '59a4286f-80ae-44ce-8e4f-d0fe8c4dd09d', 1),  -- Cheese popcorn
('aa61b3c1-5497-4cb2-987c-7a39979b5e12', '53c78d5a-9a17-42aa-bf9f-04c42a88a189', 1), -- Hot dog
('aa61b3c1-5497-4cb2-987c-7a39979b5e12', '50e16df9-7bec-451e-965b-7bbff6aa4be4', 1);  -- Medium soda (using large soda product with quantity adjustment)

-- Insert combo items for Family Bundle (combo_id 4)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', '75bb2bef-953f-47b2-8e48-6f3101515ebe', 2),  -- 2 large popcorns
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', '50e16df9-7bec-451e-965b-7bbff6aa4be4', 4),  -- 4 medium drinks (using large soda product)
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', 'b0bbe6fa-518a-4f73-ab89-84884235b513', 1),  -- M&M's
('6e57bf9f-b2a1-4f1a-86d2-1a59eee9925e', '4647a046-5ecf-4ec3-a497-75521a08e800', 1); -- Sour Patch Kids

-- Insert combo items for Ultimate Feast (combo_id 5)
INSERT INTO combo_items (combo_id, product_id, quantity) VALUES
('09330d25-b67f-4438-b615-b9d21e2bdc5f', '75bb2bef-953f-47b2-8e48-6f3101515ebe', 1),  -- Large popcorn
('09330d25-b67f-4438-b615-b9d21e2bdc5f', 'c52d2f1b-6acd-420b-9fba-8acfdc80f0ad', 1), -- Nachos
('09330d25-b67f-4438-b615-b9d21e2bdc5f', '914a5106-ac8f-43db-b482-99792e11c92e', 1), -- Chicken tenders
('09330d25-b67f-4438-b615-b9d21e2bdc5f', '50e16df9-7bec-451e-965b-7bbff6aa4be4', 2);  -- 2 large drinks
