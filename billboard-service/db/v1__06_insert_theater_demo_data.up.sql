INSERT INTO theaters (cinema_id, name, capacity, theater_type, is_active, maintenance_mode)
VALUES
(1, 'Room 1 - Main', 200, 'TWO_D', TRUE, FALSE),
(1, 'Room 2 - 3D', 160, 'THREE_D', TRUE, FALSE),
(2, 'Room 3 - IMAX', 300, 'IMAX', TRUE, FALSE),
(2, 'Room 4 - VIP', 50, 'VIP', TRUE, FALSE),
(3, 'Room 5 - 4DX', 120, 'FOUR_DX', TRUE, FALSE), 
(3, 'Room 6 - Standard', 160, 'TWO_D', FALSE, TRUE), -- No Seats
(4, 'Room 7 - Premium 3D', 150, 'THREE_D', FALSE, TRUE), -- No Seats
(4, 'Room 8 - Small', 80, 'THREE_D', FALSE, TRUE),
(5, 'Room 9 - Great Format', 280, 'IMAX', FALSE, TRUE), -- No Seats
(5, 'Room 10 - Experience', 120, 'FOUR_DX', FALSE, TRUE), -- No Seats
(6, 'Room 11 - Classic', 220, 'THREE_D', FALSE, TRUE), -- No Seats
(7, 'Room 12 - Comfort', 160, 'THREE_D', FALSE, TRUE), -- No Seats
(8, 'Room 13 - Exlusive', 70, 'VIP', FALSE, TRUE), -- No Seats
(9, 'Room 14 - Futurist', 110, 'FOUR_DX', FALSE, TRUE), -- No Seats
(10, 'Room 15 - Familiar', 190, 'THREE_D', FALSE, TRUE); -- No Seats







-- Insert 200 seats for theater_id = 1 ('Room 1 - Main')
-- Row A (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'A', 1, 'STANDARD', TRUE), (1, 'A', 2, 'STANDARD', TRUE), (1, 'A', 3, 'STANDARD', TRUE), 
(1, 'A', 4, 'STANDARD', TRUE), (1, 'A', 5, 'STANDARD', TRUE), (1, 'A', 6, 'STANDARD', TRUE), 
(1, 'A', 7, 'STANDARD', TRUE), (1, 'A', 8, 'STANDARD', TRUE), (1, 'A', 9, 'STANDARD', TRUE), 
(1, 'A', 10, 'STANDARD', TRUE), (1, 'A', 11, 'STANDARD', TRUE), (1, 'A', 12, 'STANDARD', TRUE), 
(1, 'A', 13, 'STANDARD', TRUE), (1, 'A', 14, 'STANDARD', TRUE), (1, 'A', 15, 'STANDARD', TRUE), 
(1, 'A', 16, 'STANDARD', TRUE), (1, 'A', 17, 'STANDARD', TRUE), (1, 'A', 18, 'STANDARD', TRUE), 
(1, 'A', 19, 'STANDARD', TRUE), (1, 'A', 20, 'STANDARD', TRUE);

-- Row B (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'B', 1, 'STANDARD', TRUE), (1, 'B', 2, 'STANDARD', TRUE), (1, 'B', 3, 'STANDARD', TRUE), 
(1, 'B', 4, 'STANDARD', TRUE), (1, 'B', 5, 'STANDARD', TRUE), (1, 'B', 6, 'STANDARD', TRUE), 
(1, 'B', 7, 'STANDARD', TRUE), (1, 'B', 8, 'STANDARD', TRUE), (1, 'B', 9, 'STANDARD', TRUE), 
(1, 'B', 10, 'STANDARD', TRUE), (1, 'B', 11, 'STANDARD', TRUE), (1, 'B', 12, 'STANDARD', TRUE), 
(1, 'B', 13, 'STANDARD', TRUE), (1, 'B', 14, 'STANDARD', TRUE), (1, 'B', 15, 'STANDARD', TRUE), 
(1, 'B', 16, 'STANDARD', TRUE), (1, 'B', 17, 'STANDARD', TRUE), (1, 'B', 18, 'STANDARD', TRUE), 
(1, 'B', 19, 'STANDARD', TRUE), (1, 'B', 20, 'STANDARD', TRUE);

-- Row C (8 Standard, 5 VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'C', 1, 'STANDARD', TRUE), (1, 'C', 2, 'STANDARD', TRUE), (1, 'C', 3, 'STANDARD', TRUE), 
(1, 'C', 4, 'STANDARD', TRUE), (1, 'C', 5, 'STANDARD', TRUE), (1, 'C', 6, 'STANDARD', TRUE), 
(1, 'C', 7, 'STANDARD', TRUE), (1, 'C', 8, 'STANDARD', TRUE), (1, 'C', 9, 'STANDARD', TRUE), 
(1, 'C', 10, 'STANDARD', TRUE), (1, 'C', 11, 'STANDARD', TRUE), (1, 'C', 12, 'STANDARD', TRUE), 
(1, 'C', 13, 'STANDARD', TRUE), (1, 'C', 14, 'STANDARD', TRUE), (1, 'C', 15, 'STANDARD', TRUE), 
(1, 'C', 16, 'VIP', TRUE), (1, 'C', 17, 'VIP', TRUE), (1, 'C', 18, 'VIP', TRUE), 
(1, 'C', 19, 'VIP', TRUE), (1, 'C', 20, 'VIP', TRUE);

-- Row D (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'D', 1, 'STANDARD', TRUE), (1, 'D', 2, 'STANDARD', TRUE), (1, 'D', 3, 'STANDARD', TRUE), 
(1, 'D', 4, 'STANDARD', TRUE), (1, 'D', 5, 'STANDARD', TRUE), (1, 'D', 6, 'STANDARD', TRUE), 
(1, 'D', 7, 'STANDARD', TRUE), (1, 'D', 8, 'STANDARD', TRUE), (1, 'D', 9, 'STANDARD', TRUE), 
(1, 'D', 10, 'STANDARD', TRUE), (1, 'D', 11, 'STANDARD', TRUE), (1, 'D', 12, 'STANDARD', TRUE), 
(1, 'D', 13, 'STANDARD', TRUE), (1, 'D', 14, 'STANDARD', TRUE), (1, 'D', 15, 'STANDARD', TRUE), 
(1, 'D', 16, 'STANDARD', TRUE), (1, 'D', 17, 'STANDARD', TRUE), (1, 'D', 18, 'STANDARD', TRUE), 
(1, 'D', 19, 'STANDARD', TRUE), (1, 'D', 20, 'STANDARD', TRUE);

-- Row E (8 Standard, 2 Accessible Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'E', 1, 'STANDARD', TRUE), (1, 'E', 2, 'STANDARD', TRUE), (1, 'E', 3, 'STANDARD', TRUE), 
(1, 'E', 4, 'STANDARD', TRUE), (1, 'E', 5, 'STANDARD', TRUE), (1, 'E', 6, 'STANDARD', TRUE), 
(1, 'E', 7, 'STANDARD', TRUE), (1, 'E', 8, 'STANDARD', TRUE), (1, 'E', 9, 'ACCESSIBLE', TRUE), 
(1, 'E', 10, 'ACCESSIBLE', TRUE), (1, 'E', 11, 'ACCESSIBLE', TRUE), (1, 'E', 12, 'ACCESSIBLE', TRUE), 
(1, 'E', 13, 'STANDARD', TRUE), (1, 'E', 14, 'STANDARD', TRUE), (1, 'E', 15, 'STANDARD', TRUE), 
(1, 'E', 16, 'STANDARD', TRUE), (1, 'E', 17, 'STANDARD', TRUE), (1, 'E', 18, 'STANDARD', TRUE), 
(1, 'E', 19, 'STANDARD', TRUE), (1, 'E', 20, 'STANDARD', TRUE);

-- Row F (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'F', 1, 'STANDARD', TRUE), (1, 'F', 2, 'STANDARD', TRUE), (1, 'F', 3, 'STANDARD', TRUE), 
(1, 'F', 4, 'STANDARD', TRUE), (1, 'F', 5, 'STANDARD', TRUE), (1, 'F', 6, 'STANDARD', TRUE), 
(1, 'F', 7, 'STANDARD', TRUE), (1, 'F', 8, 'STANDARD', TRUE), (1, 'F', 9, 'STANDARD', TRUE), 
(1, 'F', 10, 'STANDARD', TRUE), (1, 'F', 11, 'STANDARD', TRUE), (1, 'F', 12, 'STANDARD', TRUE), 
(1, 'F', 13, 'STANDARD', TRUE), (1, 'F', 14, 'STANDARD', TRUE), (1, 'F', 15, 'STANDARD', TRUE), 
(1, 'F', 16, 'STANDARD', TRUE), (1, 'F', 17, 'STANDARD', TRUE), (1, 'F', 18, 'STANDARD', TRUE), 
(1, 'F', 19, 'STANDARD', TRUE), (1, 'F', 20, 'STANDARD', TRUE);

-- Row G (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'G', 1, 'STANDARD', TRUE), (1, 'G', 2, 'STANDARD', TRUE), (1, 'G', 3, 'STANDARD', TRUE), 
(1, 'G', 4, 'STANDARD', TRUE), (1, 'G', 5, 'STANDARD', TRUE), (1, 'G', 6, 'STANDARD', TRUE), 
(1, 'G', 7, 'STANDARD', TRUE), (1, 'G', 8, 'STANDARD', TRUE), (1, 'G', 9, 'STANDARD', TRUE), 
(1, 'G', 10, 'STANDARD', TRUE), (1, 'G', 11, 'STANDARD', TRUE), (1, 'G', 12, 'STANDARD', TRUE), 
(1, 'G', 13, 'STANDARD', TRUE), (1, 'G', 14, 'STANDARD', TRUE), (1, 'G', 15, 'STANDARD', TRUE), 
(1, 'G', 16, 'STANDARD', TRUE), (1, 'G', 17, 'STANDARD', TRUE), (1, 'G', 18, 'STANDARD', TRUE), 
(1, 'G', 19, 'STANDARD', TRUE), (1, 'G', 20, 'STANDARD', TRUE);

-- Row H (8 Standard, 5 VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'H', 1, 'STANDARD', TRUE), (1, 'H', 2, 'STANDARD', TRUE), (1, 'H', 3, 'STANDARD', TRUE), 
(1, 'H', 4, 'STANDARD', TRUE), (1, 'H', 5, 'STANDARD', TRUE), (1, 'H', 6, 'STANDARD', TRUE), 
(1, 'H', 7, 'STANDARD', TRUE), (1, 'H', 8, 'STANDARD', TRUE), (1, 'H', 9, 'STANDARD', TRUE), 
(1, 'H', 10, 'STANDARD', TRUE), (1, 'H', 11, 'STANDARD', TRUE), (1, 'H', 12, 'STANDARD', TRUE), 
(1, 'H', 13, 'STANDARD', TRUE), (1, 'H', 14, 'STANDARD', TRUE), (1, 'H', 15, 'STANDARD', TRUE), 
(1, 'H', 16, 'VIP', TRUE), (1, 'H', 17, 'VIP', TRUE), (1, 'H', 18, 'VIP', TRUE), 
(1, 'H', 19, 'VIP', TRUE), (1, 'H', 20, 'VIP', TRUE);

-- Row I (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'I', 1, 'STANDARD', TRUE), (1, 'I', 2, 'STANDARD', TRUE), (1, 'I', 3, 'STANDARD', TRUE), 
(1, 'I', 4, 'STANDARD', TRUE), (1, 'I', 5, 'STANDARD', TRUE), (1, 'I', 6, 'STANDARD', TRUE), 
(1, 'I', 7, 'STANDARD', TRUE), (1, 'I', 8, 'STANDARD', TRUE), (1, 'I', 9, 'STANDARD', TRUE), 
(1, 'I', 10, 'STANDARD', TRUE), (1, 'I', 11, 'STANDARD', TRUE), (1, 'I', 12, 'STANDARD', TRUE), 
(1, 'I', 13, 'STANDARD', TRUE), (1, 'I', 14, 'STANDARD', TRUE), (1, 'I', 15, 'STANDARD', TRUE), 
(1, 'I', 16, 'STANDARD', TRUE), (1, 'I', 17, 'STANDARD', TRUE), (1, 'I', 18, 'STANDARD', TRUE), 
(1, 'I', 19, 'STANDARD', TRUE), (1, 'I', 20, 'STANDARD', TRUE);

-- Row J (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(1, 'J', 1, 'STANDARD', TRUE), (1, 'J', 2, 'STANDARD', TRUE), (1, 'J', 3, 'STANDARD', TRUE), 
(1, 'J', 4, 'STANDARD', TRUE), (1, 'J', 5, 'STANDARD', TRUE), (1, 'J', 6, 'STANDARD', TRUE), 
(1, 'J', 7, 'STANDARD', TRUE), (1, 'J', 8, 'STANDARD', TRUE), (1, 'J', 9, 'STANDARD', TRUE), 
(1, 'J', 10, 'STANDARD', TRUE), (1, 'J', 11, 'STANDARD', TRUE), (1, 'J', 12, 'STANDARD', TRUE), 
(1, 'J', 13, 'STANDARD', TRUE), (1, 'J', 14, 'STANDARD', TRUE), (1, 'J', 15, 'STANDARD', TRUE), 
(1, 'J', 16, 'STANDARD', TRUE), (1, 'J', 17, 'STANDARD', TRUE), (1, 'J', 18, 'STANDARD', TRUE), 
(1, 'J', 19, 'STANDARD', TRUE), (1, 'J', 20, 'STANDARD', TRUE);





-- Insert 200 seats for theater_id = 1 ('Room 2 - 3D')
-- Row A (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(2, 'A', 1, 'STANDARD', TRUE), (2, 'A', 2, 'STANDARD', TRUE), (2, 'A', 3, 'STANDARD', TRUE), 
(2, 'A', 4, 'STANDARD', TRUE), (2, 'A', 5, 'STANDARD', TRUE), (2, 'A', 6, 'STANDARD', TRUE), 
(2, 'A', 7, 'STANDARD', TRUE), (2, 'A', 8, 'STANDARD', TRUE), (2, 'A', 9, 'STANDARD', TRUE), 
(2, 'A', 10, 'STANDARD', TRUE), (2, 'A', 11, 'STANDARD', TRUE), (2, 'A', 12, 'STANDARD', TRUE), 
(2, 'A', 13, 'STANDARD', TRUE), (2, 'A', 14, 'STANDARD', TRUE), (2, 'A', 15, 'STANDARD', TRUE), 
(2, 'A', 16, 'STANDARD', TRUE), (2, 'A', 17, 'STANDARD', TRUE), (2, 'A', 18, 'STANDARD', TRUE), 
(2, 'A', 19, 'STANDARD', TRUE), (2, 'A', 20, 'STANDARD', TRUE);

-- Row B (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(2, 'B', 1, 'STANDARD', TRUE), (2, 'B', 2, 'STANDARD', TRUE), (2, 'B', 3, 'STANDARD', TRUE), 
(2, 'B', 4, 'STANDARD', TRUE), (2, 'B', 5, 'STANDARD', TRUE), (2, 'B', 6, 'STANDARD', TRUE),
(2, 'B', 7, 'STANDARD', TRUE), (2, 'B', 8, 'STANDARD', TRUE), (2, 'B', 9, 'STANDARD', TRUE), 
(2, 'B', 10, 'STANDARD', TRUE), (2, 'B', 11, 'STANDARD', TRUE), (2, 'B', 12, 'STANDARD', TRUE), 
(2, 'B', 13, 'STANDARD', TRUE), (2, 'B', 14, 'STANDARD', TRUE), (2, 'B', 15, 'STANDARD', TRUE), 
(2, 'B', 16, 'STANDARD', TRUE), (2, 'B', 17, 'STANDARD', TRUE), (2, 'B', 18, 'STANDARD', TRUE), 
(2, 'B', 19, 'STANDARD', TRUE), (2, 'B', 20, 'STANDARD', TRUE);

-- Row C (8 Standard, 5 VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(2, 'C', 1, 'STANDARD', TRUE), (2, 'C', 2, 'STANDARD', TRUE), (2, 'C', 3, 'STANDARD', TRUE), 
(2, 'C', 4, 'STANDARD', TRUE), (2, 'C', 5, 'STANDARD', TRUE), (2, 'C', 6, 'STANDARD', TRUE), 
(2, 'C', 7, 'STANDARD', TRUE), (2, 'C', 8, 'STANDARD', TRUE), (2, 'C', 9, 'STANDARD', TRUE), 
(2, 'C', 10, 'STANDARD', TRUE), (2, 'C', 11, 'STANDARD', TRUE), (2, 'C', 12, 'STANDARD', TRUE), 
(2, 'C', 13, 'STANDARD', TRUE), (2, 'C', 14, 'STANDARD', TRUE), (2, 'C', 15, 'STANDARD', TRUE), 
(2, 'C', 16, 'VIP', TRUE), (2, 'C', 17, 'VIP', TRUE), (2, 'C', 18, 'VIP', TRUE), 
(2, 'C', 19, 'VIP', TRUE), (2, 'C', 20, 'VIP', TRUE);

-- Row D (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(2, 'D', 1, 'STANDARD', TRUE), (2, 'D', 2, 'STANDARD', TRUE), (2, 'D', 3, 'STANDARD', TRUE), 
(2, 'D', 4, 'STANDARD', TRUE), (2, 'D', 5, 'STANDARD', TRUE), (2, 'D', 6, 'STANDARD', TRUE), 
(2, 'D', 7, 'STANDARD', TRUE), (2, 'D', 8, 'STANDARD', TRUE), (2, 'D', 9, 'STANDARD', TRUE), 
(2, 'D', 10, 'STANDARD', TRUE), (2, 'D', 11, 'STANDARD', TRUE), (2, 'D', 12, 'STANDARD', TRUE), 
(2, 'D', 13, 'STANDARD', TRUE), (2, 'D', 14, 'STANDARD', TRUE), (2, 'D', 15, 'STANDARD', TRUE), 
(2, 'D', 16, 'STANDARD', TRUE), (2, 'D', 17, 'STANDARD', TRUE), (2, 'D', 18, 'STANDARD', TRUE), 
(2, 'D', 19, 'STANDARD', TRUE), (2, 'D', 20, 'STANDARD', TRUE);

-- Row E (8 Standard, 2 Accessible Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(2, 'E', 1, 'STANDARD', TRUE), (2, 'E', 2, 'STANDARD', TRUE), (2, 'E', 3, 'STANDARD', TRUE), 
(2, 'E', 4, 'STANDARD', TRUE), (2, 'E', 5, 'STANDARD', TRUE), (2, 'E', 6, 'STANDARD', TRUE), 
(2, 'E', 7, 'STANDARD', TRUE), (2, 'E', 8, 'STANDARD', TRUE), (2, 'E', 9, 'ACCESSIBLE', TRUE),
(2, 'E', 10, 'ACCESSIBLE', TRUE), (2, 'E', 11, 'ACCESSIBLE', TRUE), (2, 'E', 12, 'ACCESSIBLE', TRUE), 
(2, 'E', 13, 'STANDARD', TRUE), (2, 'E', 14, 'STANDARD', TRUE), (2, 'E', 15, 'STANDARD', TRUE), 
(2, 'E', 16, 'STANDARD', TRUE), (2, 'E', 17, 'STANDARD', TRUE), (2, 'E', 18, 'STANDARD', TRUE), 
(2, 'E', 19, 'STANDARD', TRUE), (2, 'E', 20, 'STANDARD', TRUE);

-- Row F (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(2, 'F', 1, 'STANDARD', TRUE), (2, 'F', 2, 'STANDARD', TRUE), (2, 'F', 3, 'STANDARD', TRUE), 
(2, 'F', 4, 'STANDARD', TRUE), (2, 'F', 5, 'STANDARD', TRUE), (2, 'F', 6, 'STANDARD', TRUE), 
(2, 'F', 7, 'STANDARD', TRUE), (2, 'F', 8, 'STANDARD', TRUE), (2, 'F', 9, 'STANDARD', TRUE), 
(2, 'F', 10, 'STANDARD', TRUE), (2, 'F', 11, 'STANDARD', TRUE), (2, 'F', 12, 'STANDARD', TRUE), 
(2, 'F', 13, 'STANDARD', TRUE), (2, 'F', 14, 'STANDARD', TRUE), (2, 'F', 15, 'STANDARD', TRUE), 
(2, 'F', 16, 'STANDARD', TRUE), (2, 'F', 17, 'STANDARD', TRUE), (2, 'F', 18, 'STANDARD', TRUE), 
(2, 'F', 19, 'STANDARD', TRUE), (2, 'F', 20, 'STANDARD', TRUE);

-- Row G (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(2, 'G', 1, 'STANDARD', TRUE), (2, 'G', 2, 'STANDARD', TRUE), (2, 'G', 3, 'STANDARD', TRUE), 
(2, 'G', 4, 'STANDARD', TRUE), (2, 'G', 5, 'STANDARD', TRUE), (2, 'G', 6, 'STANDARD', TRUE), 
(2, 'G', 7, 'STANDARD', TRUE), (2, 'G', 8, 'STANDARD', TRUE), (2, 'G', 9, 'STANDARD', TRUE), 
(2, 'G', 10, 'STANDARD', TRUE), (2, 'G', 11, 'STANDARD', TRUE), (2, 'G', 12, 'STANDARD', TRUE), 
(2, 'G', 13, 'STANDARD', TRUE), (2, 'G', 14, 'STANDARD', TRUE), (2, 'G', 15, 'STANDARD', TRUE), 
(2, 'G', 16, 'STANDARD', TRUE), (2, 'G', 17, 'STANDARD', TRUE), (2, 'G', 18, 'STANDARD', TRUE), 
(2, 'G', 19, 'STANDARD', TRUE), (2, 'G', 20, 'STANDARD', TRUE);

-- Row H (8 Standard, 5 VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(2, 'H', 1, 'STANDARD', TRUE), (2, 'H', 2, 'STANDARD', TRUE), (2, 'H', 3, 'STANDARD', TRUE), 
(2, 'H', 4, 'STANDARD', TRUE), (2, 'H', 5, 'STANDARD', TRUE), (2, 'H', 6, 'STANDARD', TRUE), 
(2, 'H', 7, 'STANDARD', TRUE), (2, 'H', 8, 'STANDARD', TRUE), (2, 'H', 9, 'STANDARD', TRUE), 
(2, 'H', 10, 'STANDARD', TRUE), (2, 'H', 11, 'STANDARD', TRUE), (2, 'H', 12, 'STANDARD', TRUE), 
(2, 'H', 13, 'STANDARD', TRUE), (2, 'H', 14, 'STANDARD', TRUE), (2, 'H', 15, 'STANDARD', TRUE), 
(2, 'H', 16, 'VIP', TRUE), (2, 'H', 17, 'VIP', TRUE), (2, 'H', 18, 'VIP', TRUE), 
(2, 'H', 19, 'VIP', TRUE), (2, 'H', 20, 'VIP', TRUE);





-- Insert 300 seats for theater_id = 3 ('Room 3 - IMAX')
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(3, 'A', 1, 'STANDARD', TRUE), (3, 'A', 2, 'STANDARD', TRUE), (3, 'A', 3, 'STANDARD', TRUE), 
(3, 'A', 4, 'STANDARD', TRUE), (3, 'A', 5, 'STANDARD', TRUE), (3, 'A', 6, 'STANDARD', TRUE), 
(3, 'A', 7, 'STANDARD', TRUE), (3, 'A', 8, 'STANDARD', TRUE), (3, 'A', 9, 'STANDARD', TRUE), 
(3, 'A', 10, 'STANDARD', TRUE), (3, 'A', 11, 'STANDARD', TRUE), (3, 'A', 12, 'STANDARD', TRUE), 
(3, 'A', 13, 'STANDARD', TRUE), (3, 'A', 14, 'STANDARD', TRUE), (3, 'A', 15, 'STANDARD', TRUE), 
(3, 'A', 16, 'STANDARD', TRUE), (3, 'A', 17, 'STANDARD', TRUE), (3, 'A', 18, 'STANDARD', TRUE), 
(3, 'A', 19, 'STANDARD', TRUE), (3, 'A', 20, 'STANDARD', TRUE), (3, 'A', 21, 'STANDARD', TRUE),  (3, 'A', 22, 'STANDARD', TRUE), 
(3, 'A', 23, 'STANDARD', TRUE), (3, 'A', 24, 'STANDARD', TRUE), (3, 'A', 25, 'STANDARD', TRUE);

-- Row B (20 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES 
(3, 'B', 1, 'STANDARD', TRUE), (3, 'B', 2, 'STANDARD', TRUE), (3, 'B', 3, 'STANDARD', TRUE), 
(3, 'B', 4, 'STANDARD', TRUE), (3, 'B', 5, 'STANDARD', TRUE), (3, 'B', 6, 'STANDARD', TRUE), 
(3, 'B', 7, 'STANDARD', TRUE), (3, 'B', 8, 'STANDARD', TRUE), (3, 'B', 9, 'STANDARD', TRUE), 
(3, 'B', 10, 'STANDARD', TRUE), (3, 'B', 11, 'STANDARD', TRUE), (3, 'B', 12, 'STANDARD', TRUE), 
(3, 'B', 13, 'STANDARD', TRUE), (3, 'B', 14, 'STANDARD', TRUE), (3, 'B', 15, 'STANDARD', TRUE), 
(3, 'B', 16, 'STANDARD', TRUE), (3, 'B', 17, 'STANDARD', TRUE), (3, 'B', 18, 'STANDARD', TRUE), 
(3, 'B', 19, 'STANDARD', TRUE), (3, 'B', 20, 'STANDARD', TRUE), (3, 'B', 21, 'STANDARD', TRUE), 
(3, 'B', 22, 'STANDARD', TRUE), (3, 'B', 23, 'STANDARD', TRUE), (3, 'B', 24, 'STANDARD', TRUE), (3, 'B', 25, 'STANDARD', TRUE);

-- Row C (20 Standard, 5 VIP Seats, total 25 seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'C', 1, 'STANDARD', TRUE), (3, 'C', 2, 'STANDARD', TRUE), (3, 'C', 3, 'STANDARD', TRUE),
(3, 'C', 4, 'STANDARD', TRUE), (3, 'C', 5, 'STANDARD', TRUE), (3, 'C', 6, 'STANDARD', TRUE),
(3, 'C', 7, 'STANDARD', TRUE), (3, 'C', 8, 'STANDARD', TRUE), (3, 'C', 9, 'STANDARD', TRUE),
(3, 'C', 10, 'STANDARD', TRUE), (3, 'C', 11, 'STANDARD', TRUE), (3, 'C', 12, 'STANDARD', TRUE),
(3, 'C', 13, 'STANDARD', TRUE), (3, 'C', 14, 'STANDARD', TRUE), (3, 'C', 15, 'STANDARD', TRUE),
(3, 'C', 16, 'STANDARD', TRUE), (3, 'C', 17, 'STANDARD', TRUE), (3, 'C', 18, 'STANDARD', TRUE),
(3, 'C', 19, 'STANDARD', TRUE), (3, 'C', 20, 'STANDARD', TRUE),
(3, 'C', 21, 'VIP', TRUE), (3, 'C', 22, 'VIP', TRUE), (3, 'C', 23, 'VIP', TRUE),
(3, 'C', 24, 'VIP', TRUE), (3, 'C', 25, 'VIP', TRUE);

-- Row D (25 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'D', 1, 'STANDARD', TRUE), (3, 'D', 2, 'STANDARD', TRUE), (3, 'D', 3, 'STANDARD', TRUE),
(3, 'D', 4, 'STANDARD', TRUE), (3, 'D', 5, 'STANDARD', TRUE), (3, 'D', 6, 'STANDARD', TRUE),
(3, 'D', 7, 'STANDARD', TRUE), (3, 'D', 8, 'STANDARD', TRUE), (3, 'D', 9, 'STANDARD', TRUE),
(3, 'D', 10, 'STANDARD', TRUE), (3, 'D', 11, 'STANDARD', TRUE), (3, 'D', 12, 'STANDARD', TRUE),
(3, 'D', 13, 'STANDARD', TRUE), (3, 'D', 14, 'STANDARD', TRUE), (3, 'D', 15, 'STANDARD', TRUE),
(3, 'D', 16, 'STANDARD', TRUE), (3, 'D', 17, 'STANDARD', TRUE), (3, 'D', 18, 'STANDARD', TRUE),
(3, 'D', 19, 'STANDARD', TRUE), (3, 'D', 20, 'STANDARD', TRUE), (3, 'D', 21, 'STANDARD', TRUE),
(3, 'D', 22, 'STANDARD', TRUE), (3, 'D', 23, 'STANDARD', TRUE), (3, 'D', 24, 'STANDARD', TRUE),
(3, 'D', 25, 'STANDARD', TRUE);

-- Row E (20 Standard, 5 Accessible Seats, total 25 seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'E', 1, 'STANDARD', TRUE), (3, 'E', 2, 'STANDARD', TRUE), (3, 'E', 3, 'STANDARD', TRUE),
(3, 'E', 4, 'STANDARD', TRUE), (3, 'E', 5, 'STANDARD', TRUE), (3, 'E', 6, 'STANDARD', TRUE),
(3, 'E', 7, 'STANDARD', TRUE), (3, 'E', 8, 'STANDARD', TRUE), (3, 'E', 9, 'STANDARD', TRUE),
(3, 'E', 10, 'STANDARD', TRUE), (3, 'E', 11, 'STANDARD', TRUE), (3, 'E', 12, 'STANDARD', TRUE),
(3, 'E', 13, 'STANDARD', TRUE), (3, 'E', 14, 'STANDARD', TRUE), (3, 'E', 15, 'STANDARD', TRUE),
(3, 'E', 16, 'STANDARD', TRUE), (3, 'E', 17, 'STANDARD', TRUE), (3, 'E', 18, 'STANDARD', TRUE),
(3, 'E', 19, 'STANDARD', TRUE), (3, 'E', 20, 'STANDARD', TRUE),
(3, 'E', 21, 'ACCESSIBLE', TRUE), (3, 'E', 22, 'ACCESSIBLE', TRUE), (3, 'E', 23, 'ACCESSIBLE', TRUE),
(3, 'E', 24, 'ACCESSIBLE', TRUE), (3, 'E', 25, 'ACCESSIBLE', TRUE);

-- Row F (25 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'F', 1, 'STANDARD', TRUE), (3, 'F', 2, 'STANDARD', TRUE), (3, 'F', 3, 'STANDARD', TRUE),
(3, 'F', 4, 'STANDARD', TRUE), (3, 'F', 5, 'STANDARD', TRUE), (3, 'F', 6, 'STANDARD', TRUE),
(3, 'F', 7, 'STANDARD', TRUE), (3, 'F', 8, 'STANDARD', TRUE), (3, 'F', 9, 'STANDARD', TRUE),
(3, 'F', 10, 'STANDARD', TRUE), (3, 'F', 11, 'STANDARD', TRUE), (3, 'F', 12, 'STANDARD', TRUE),
(3, 'F', 13, 'STANDARD', TRUE), (3, 'F', 14, 'STANDARD', TRUE), (3, 'F', 15, 'STANDARD', TRUE),
(3, 'F', 16, 'STANDARD', TRUE), (3, 'F', 17, 'STANDARD', TRUE), (3, 'F', 18, 'STANDARD', TRUE),
(3, 'F', 19, 'STANDARD', TRUE), (3, 'F', 20, 'STANDARD', TRUE), (3, 'F', 21, 'STANDARD', TRUE),
(3, 'F', 22, 'STANDARD', TRUE), (3, 'F', 23, 'STANDARD', TRUE), (3, 'F', 24, 'STANDARD', TRUE),
(3, 'F', 25, 'STANDARD', TRUE);

-- Row G (25 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'G', 1, 'STANDARD', TRUE), (3, 'G', 2, 'STANDARD', TRUE), (3, 'G', 3, 'STANDARD', TRUE),
(3, 'G', 4, 'STANDARD', TRUE), (3, 'G', 5, 'STANDARD', TRUE), (3, 'G', 6, 'STANDARD', TRUE),
(3, 'G', 7, 'STANDARD', TRUE), (3, 'G', 8, 'STANDARD', TRUE), (3, 'G', 9, 'STANDARD', TRUE),
(3, 'G', 10, 'STANDARD', TRUE), (3, 'G', 11, 'STANDARD', TRUE), (3, 'G', 12, 'STANDARD', TRUE),
(3, 'G', 13, 'STANDARD', TRUE), (3, 'G', 14, 'STANDARD', TRUE), (3, 'G', 15, 'STANDARD', TRUE),
(3, 'G', 16, 'STANDARD', TRUE), (3, 'G', 17, 'STANDARD', TRUE), (3, 'G', 18, 'STANDARD', TRUE),
(3, 'G', 19, 'STANDARD', TRUE), (3, 'G', 20, 'STANDARD', TRUE), (3, 'G', 21, 'STANDARD', TRUE),
(3, 'G', 22, 'STANDARD', TRUE), (3, 'G', 23, 'STANDARD', TRUE), (3, 'G', 24, 'STANDARD', TRUE),
(3, 'G', 25, 'STANDARD', TRUE);

-- Row H (20 Standard, 5 VIP Seats, total 25 seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'H', 1, 'STANDARD', TRUE), (3, 'H', 2, 'STANDARD', TRUE), (3, 'H', 3, 'STANDARD', TRUE),
(3, 'H', 4, 'STANDARD', TRUE), (3, 'H', 5, 'STANDARD', TRUE), (3, 'H', 6, 'STANDARD', TRUE),
(3, 'H', 7, 'STANDARD', TRUE), (3, 'H', 8, 'STANDARD', TRUE), (3, 'H', 9, 'STANDARD', TRUE),
(3, 'H', 10, 'STANDARD', TRUE), (3, 'H', 11, 'STANDARD', TRUE), (3, 'H', 12, 'STANDARD', TRUE),
(3, 'H', 13, 'STANDARD', TRUE), (3, 'H', 14, 'STANDARD', TRUE), (3, 'H', 15, 'STANDARD', TRUE),
(3, 'H', 16, 'STANDARD', TRUE), (3, 'H', 17, 'STANDARD', TRUE), (3, 'H', 18, 'STANDARD', TRUE),
(3, 'H', 19, 'STANDARD', TRUE), (3, 'H', 20, 'STANDARD', TRUE),
(3, 'H', 21, 'VIP', TRUE), (3, 'H', 22, 'VIP', TRUE), (3, 'H', 23, 'VIP', TRUE),
(3, 'H', 24, 'VIP', TRUE), (3, 'H', 25, 'VIP', TRUE);

-- Row I (25 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'I', 1, 'STANDARD', TRUE), (3, 'I', 2, 'STANDARD', TRUE), (3, 'I', 3, 'STANDARD', TRUE),
(3, 'I', 4, 'STANDARD', TRUE), (3, 'I', 5, 'STANDARD', TRUE), (3, 'I', 6, 'STANDARD', TRUE),
(3, 'I', 7, 'STANDARD', TRUE), (3, 'I', 8, 'STANDARD', TRUE), (3, 'I', 9, 'STANDARD', TRUE),
(3, 'I', 10, 'STANDARD', TRUE), (3, 'I', 11, 'STANDARD', TRUE), (3, 'I', 12, 'STANDARD', TRUE),
(3, 'I', 13, 'STANDARD', TRUE), (3, 'I', 14, 'STANDARD', TRUE), (3, 'I', 15, 'STANDARD', TRUE),
(3, 'I', 16, 'STANDARD', TRUE), (3, 'I', 17, 'STANDARD', TRUE), (3, 'I', 18, 'STANDARD', TRUE),
(3, 'I', 19, 'STANDARD', TRUE), (3, 'I', 20, 'STANDARD', TRUE), (3, 'I', 21, 'STANDARD', TRUE),
(3, 'I', 22, 'STANDARD', TRUE), (3, 'I', 23, 'STANDARD', TRUE), (3, 'I', 24, 'STANDARD', TRUE),
(3, 'I', 25, 'STANDARD', TRUE);

-- Row J (25 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'J', 1, 'STANDARD', TRUE), (3, 'J', 2, 'STANDARD', TRUE), (3, 'J', 3, 'STANDARD', TRUE),
(3, 'J', 4, 'STANDARD', TRUE), (3, 'J', 5, 'STANDARD', TRUE), (3, 'J', 6, 'STANDARD', TRUE),
(3, 'J', 7, 'STANDARD', TRUE), (3, 'J', 8, 'STANDARD', TRUE), (3, 'J', 9, 'STANDARD', TRUE),
(3, 'J', 10, 'STANDARD', TRUE), (3, 'J', 11, 'STANDARD', TRUE), (3, 'J', 12, 'STANDARD', TRUE),
(3, 'J', 13, 'STANDARD', TRUE), (3, 'J', 14, 'STANDARD', TRUE), (3, 'J', 15, 'STANDARD', TRUE),
(3, 'J', 16, 'STANDARD', TRUE), (3, 'J', 17, 'STANDARD', TRUE), (3, 'J', 18, 'STANDARD', TRUE),
(3, 'J', 19, 'STANDARD', TRUE), (3, 'J', 20, 'STANDARD', TRUE), (3, 'J', 21, 'STANDARD', TRUE),
(3, 'J', 22, 'STANDARD', TRUE), (3, 'J', 23, 'STANDARD', TRUE), (3, 'J', 24, 'STANDARD', TRUE),
(3, 'J', 25, 'STANDARD', TRUE);

-- Row K (25 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'K', 1, 'STANDARD', TRUE), (3, 'K', 2, 'STANDARD', TRUE), (3, 'K', 3, 'STANDARD', TRUE),
(3, 'K', 4, 'STANDARD', TRUE), (3, 'K', 5, 'STANDARD', TRUE), (3, 'K', 6, 'STANDARD', TRUE),
(3, 'K', 7, 'STANDARD', TRUE), (3, 'K', 8, 'STANDARD', TRUE), (3, 'K', 9, 'STANDARD', TRUE),
(3, 'K', 10, 'STANDARD', TRUE), (3, 'K', 11, 'STANDARD', TRUE), (3, 'K', 12, 'STANDARD', TRUE),
(3, 'K', 13, 'STANDARD', TRUE), (3, 'K', 14, 'STANDARD', TRUE), (3, 'K', 15, 'STANDARD', TRUE),
(3, 'K', 16, 'STANDARD', TRUE), (3, 'K', 17, 'STANDARD', TRUE), (3, 'K', 18, 'STANDARD', TRUE),
(3, 'K', 19, 'STANDARD', TRUE), (3, 'K', 20, 'STANDARD', TRUE), (3, 'K', 21, 'STANDARD', TRUE),
(3, 'K', 22, 'STANDARD', TRUE), (3, 'K', 23, 'STANDARD', TRUE), (3, 'K', 24, 'STANDARD', TRUE),
(3, 'K', 25, 'STANDARD', TRUE);

-- Row L (20 Standard, 5 Premium Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'L', 1, 'STANDARD', TRUE), (3, 'L', 2, 'STANDARD', TRUE), (3, 'L', 3, 'STANDARD', TRUE),
(3, 'L', 4, 'STANDARD', TRUE), (3, 'L', 5, 'STANDARD', TRUE), (3, 'L', 6, 'STANDARD', TRUE),
(3, 'L', 7, 'STANDARD', TRUE), (3, 'L', 8, 'STANDARD', TRUE), (3, 'L', 9, 'STANDARD', TRUE),
(3, 'L', 10, 'STANDARD', TRUE), (3, 'L', 11, 'STANDARD', TRUE), (3, 'L', 12, 'STANDARD', TRUE),
(3, 'L', 13, 'STANDARD', TRUE), (3, 'L', 14, 'STANDARD', TRUE), (3, 'L', 15, 'STANDARD', TRUE),
(3, 'L', 16, 'STANDARD', TRUE), (3, 'L', 17, 'STANDARD', TRUE), (3, 'L', 18, 'STANDARD', TRUE),
(3, 'L', 19, 'STANDARD', TRUE), (3, 'L', 20, 'STANDARD', TRUE), (3, 'L', 21, 'PREMIUM', TRUE),
(3, 'L', 22, 'PREMIUM', TRUE), (3, 'L', 23, 'PREMIUM', TRUE), (3, 'L', 24, 'PREMIUM', TRUE),
(3, 'L', 25, 'PREMIUM', TRUE);

-- Row M (25 Standard Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'M', 1, 'STANDARD', TRUE), (3, 'M', 2, 'STANDARD', TRUE), (3, 'M', 3, 'STANDARD', TRUE),
(3, 'M', 4, 'STANDARD', TRUE), (3, 'M', 5, 'STANDARD', TRUE), (3, 'M', 6, 'STANDARD', TRUE),
(3, 'M', 7, 'STANDARD', TRUE), (3, 'M', 8, 'STANDARD', TRUE), (3, 'M', 9, 'STANDARD', TRUE),
(3, 'M', 10, 'STANDARD', TRUE), (3, 'M', 11, 'STANDARD', TRUE), (3, 'M', 12, 'STANDARD', TRUE),
(3, 'M', 13, 'STANDARD', TRUE), (3, 'M', 14, 'STANDARD', TRUE), (3, 'M', 15, 'STANDARD', TRUE),
(3, 'M', 16, 'STANDARD', TRUE), (3, 'M', 17, 'STANDARD', TRUE), (3, 'M', 18, 'STANDARD', TRUE),
(3, 'M', 19, 'STANDARD', TRUE), (3, 'M', 20, 'STANDARD', TRUE), (3, 'M', 21, 'STANDARD', TRUE),
(3, 'M', 22, 'STANDARD', TRUE), (3, 'M', 23, 'STANDARD', TRUE), (3, 'M', 24, 'STANDARD', TRUE),
(3, 'M', 25, 'STANDARD', TRUE);

-- Row N (20 Standard, 5 Accessible Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(3, 'N', 1, 'STANDARD', TRUE), (3, 'N', 2, 'STANDARD', TRUE), (3, 'N', 3, 'STANDARD', TRUE),
(3, 'N', 4, 'STANDARD', TRUE), (3, 'N', 5, 'STANDARD', TRUE), (3, 'N', 6, 'STANDARD', TRUE),
(3, 'N', 7, 'STANDARD', TRUE), (3, 'N', 8, 'STANDARD', TRUE), (3, 'N', 9, 'STANDARD', TRUE),
(3, 'N', 10, 'STANDARD', TRUE), (3, 'N', 11, 'STANDARD', TRUE), (3, 'N', 12, 'STANDARD', TRUE),
(3, 'N', 13, 'STANDARD', TRUE), (3, 'N', 14, 'STANDARD', TRUE), (3, 'N', 15, 'STANDARD', TRUE),
(3, 'N', 16, 'STANDARD', TRUE), (3, 'N', 17, 'STANDARD', TRUE), (3, 'N', 18, 'STANDARD', TRUE),
(3, 'N', 19, 'STANDARD', TRUE), (3, 'N', 20, 'STANDARD', TRUE), (3, 'N', 21, 'ACCESSIBLE', TRUE),
(3, 'N', 22, 'ACCESSIBLE', TRUE), (3, 'N', 23, 'ACCESSIBLE', TRUE), (3, 'N', 24, 'ACCESSIBLE', TRUE),
(3, 'N', 25, 'ACCESSIBLE', TRUE);







-- 50 seats for theater_id = 5 (New Theater, starting rows from A)
-- Row A (10 VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(4, 'A', 1, 'VIP', TRUE), (4, 'A', 2, 'VIP', TRUE), (4, 'A', 3, 'VIP', TRUE),
(4, 'A', 4, 'VIP', TRUE), (4, 'A', 5, 'VIP', TRUE), (4, 'A', 6, 'VIP', TRUE),
(4, 'A', 7, 'VIP', TRUE), (4, 'A', 8, 'VIP', TRUE), (4, 'A', 9, 'VIP', TRUE),
(4, 'A', 10, 'VIP', TRUE);

-- Row B (10 VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(4, 'B', 1, 'VIP', TRUE), (4, 'B', 2, 'VIP', TRUE), (4, 'B', 3, 'VIP', TRUE),
(4, 'B', 4, 'VIP', TRUE), (4, 'B', 5, 'VIP', TRUE), (4, 'B', 6, 'VIP', TRUE),
(4, 'B', 7, 'VIP', TRUE), (4, 'B', 8, 'VIP', TRUE), (4, 'B', 9, 'VIP', TRUE),
(4, 'B', 10, 'VIP', TRUE);

-- Row C (10 VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(4, 'C', 1, 'VIP', TRUE), (4, 'C', 2, 'VIP', TRUE), (4, 'C', 3, 'VIP', TRUE),
(4, 'C', 4, 'VIP', TRUE), (4, 'C', 5, 'VIP', TRUE), (4, 'C', 6, 'VIP', TRUE),
(4, 'C', 7, 'VIP', TRUE), (4, 'C', 8, 'VIP', TRUE), (4, 'C', 9, 'VIP', TRUE),
(4, 'C', 10, 'VIP', TRUE);

-- Row D (8 VIP Seats, 2 Accessible VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(4, 'D', 1, 'VIP', TRUE), (4, 'D', 2, 'VIP', TRUE), (4, 'D', 3, 'VIP', TRUE),
(4, 'D', 4, 'VIP', TRUE), (4, 'D', 5, 'VIP', TRUE), (4, 'D', 6, 'VIP', TRUE),
(4, 'D', 7, 'VIP', TRUE), (4, 'D', 8, 'VIP', TRUE),
(4, 'D', 9, 'ACCESSIBLE', TRUE), -- Accessible VIP seating
(4, 'D', 10, 'ACCESSIBLE', TRUE); -- Accessible VIP seating

-- Row E (10 VIP Seats)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(4, 'E', 1, 'VIP', TRUE), (4, 'E', 2, 'VIP', TRUE), (4, 'E', 3, 'VIP', TRUE),
(4, 'E', 4, 'VIP', TRUE), (4, 'E', 5, 'VIP', TRUE), (4, 'E', 6, 'VIP', TRUE),
(4, 'E', 7, 'VIP', TRUE), (4, 'E', 8, 'VIP', TRUE), (4, 'E', 9, 'VIP', TRUE),
(4, 'E', 10, 'VIP', TRUE);






-- Seats for theater_id = 5 ('Room 5 - 4DX')
-- Rows A-J: 10 seats per row (100 seats total)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(5, 'A', 1, 'FOUR_DX', TRUE), (5, 'A', 2, 'FOUR_DX', TRUE), (5, 'A', 3, 'FOUR_DX', TRUE), 
(5, 'A', 4, 'FOUR_DX', TRUE), (5, 'A', 5, 'FOUR_DX', TRUE), (5, 'A', 6, 'FOUR_DX', TRUE), 
(5, 'A', 7, 'FOUR_DX', TRUE), (5, 'A', 8, 'FOUR_DX', TRUE), (5, 'A', 9, 'FOUR_DX', TRUE), 
(5, 'A', 10, 'FOUR_DX', TRUE),

(5, 'B', 1, 'FOUR_DX', TRUE), (5, 'B', 2, 'FOUR_DX', TRUE), (5, 'B', 3, 'FOUR_DX', TRUE), 
(5, 'B', 4, 'FOUR_DX', TRUE), (5, 'B', 5, 'FOUR_DX', TRUE), (5, 'B', 6, 'FOUR_DX', TRUE), 
(5, 'B', 7, 'FOUR_DX', TRUE), (5, 'B', 8, 'FOUR_DX', TRUE), (5, 'B', 9, 'FOUR_DX', TRUE),
(5, 'B', 10, 'FOUR_DX', TRUE),

(5, 'C', 1, 'FOUR_DX', TRUE), (5, 'C', 2, 'FOUR_DX', TRUE), (5, 'C', 3, 'FOUR_DX', TRUE), 
(5, 'C', 4, 'FOUR_DX', TRUE), (5, 'C', 5, 'FOUR_DX', TRUE), (5, 'C', 6, 'FOUR_DX', TRUE), 
(5, 'C', 7, 'FOUR_DX', TRUE), (5, 'C', 8, 'FOUR_DX', TRUE), (5, 'C', 9, 'FOUR_DX', TRUE), 
(5, 'C', 10, 'FOUR_DX', TRUE),

(5, 'D', 1, 'FOUR_DX', TRUE), (5, 'D', 2, 'FOUR_DX', TRUE), (5, 'D', 3, 'FOUR_DX', TRUE), 
(5, 'D', 4, 'FOUR_DX', TRUE), (5, 'D', 5, 'FOUR_DX', TRUE), (5, 'D', 6, 'FOUR_DX', TRUE), 
(5, 'D', 7, 'FOUR_DX', TRUE), (5, 'D', 8, 'FOUR_DX', TRUE), (5, 'D', 9, 'FOUR_DX', TRUE), 
(5, 'D', 10, 'FOUR_DX', TRUE), 

(5, 'E', 1, 'FOUR_DX', TRUE), (5, 'E', 2, 'FOUR_DX', TRUE), (5, 'E', 3, 'FOUR_DX', TRUE), 
(5, 'E', 4, 'FOUR_DX', TRUE), (5, 'E', 5, 'FOUR_DX', TRUE), (5, 'E', 6, 'FOUR_DX', TRUE), 
(5, 'E', 7, 'FOUR_DX', TRUE), (5, 'E', 8, 'FOUR_DX', TRUE), (5, 'E', 9, 'FOUR_DX', TRUE), 
(5, 'E', 10, 'FOUR_DX', TRUE),

(5, 'F', 1, 'FOUR_DX', TRUE), (5, 'F', 2, 'FOUR_DX', TRUE), (5, 'F', 3, 'FOUR_DX', TRUE), 
(5, 'F', 4, 'FOUR_DX', TRUE), (5, 'F', 5, 'FOUR_DX', TRUE), (5, 'F', 6, 'FOUR_DX', TRUE), 
(5, 'F', 7, 'FOUR_DX', TRUE), (5, 'F', 8, 'FOUR_DX', TRUE), (5, 'F', 9, 'FOUR_DX', TRUE), 
(5, 'F', 10, 'FOUR_DX', TRUE), 

(5, 'G', 1, 'FOUR_DX', TRUE), (5, 'G', 2, 'FOUR_DX', TRUE), (5, 'G', 3, 'FOUR_DX', TRUE), 
(5, 'G', 4, 'FOUR_DX', TRUE), (5, 'G', 5, 'FOUR_DX', TRUE), (5, 'G', 6, 'FOUR_DX', TRUE), 
(5, 'G', 7, 'FOUR_DX', TRUE), (5, 'G', 8, 'FOUR_DX', TRUE),  (5, 'G', 9, 'FOUR_DX', TRUE), 
(5, 'G', 10, 'FOUR_DX', TRUE),

(5, 'H', 1, 'FOUR_DX', TRUE), (5, 'H', 2, 'FOUR_DX', TRUE), (5, 'H', 3, 'FOUR_DX', TRUE), 
(5, 'H', 4, 'FOUR_DX', TRUE), 
(5, 'H', 5, 'FOUR_DX', TRUE), (5, 'H', 6, 'FOUR_DX', TRUE), (5, 'H', 7, 'FOUR_DX', TRUE), 
(5, 'H', 8, 'FOUR_DX', TRUE), (5, 'H', 9, 'FOUR_DX', TRUE), (5, 'H', 10, 'FOUR_DX', TRUE),

(5, 'I', 1, 'FOUR_DX', TRUE), (5, 'I', 2, 'FOUR_DX', TRUE), (5, 'I', 3, 'FOUR_DX', TRUE), 
(5, 'I', 4, 'FOUR_DX', TRUE), (5, 'I', 5, 'FOUR_DX', TRUE), (5, 'I', 6, 'FOUR_DX', TRUE), 
(5, 'I', 7, 'FOUR_DX', TRUE), (5, 'I', 8, 'FOUR_DX', TRUE), (5, 'I', 9, 'FOUR_DX', TRUE), 
(5, 'I', 10, 'FOUR_DX', TRUE),

(5, 'J', 1, 'FOUR_DX', TRUE), (5, 'J', 2, 'FOUR_DX', TRUE), (5, 'J', 3, 'FOUR_DX', TRUE), 
(5, 'J', 4, 'FOUR_DX', TRUE), (5, 'J', 5, 'FOUR_DX', TRUE), (5, 'J', 6, 'FOUR_DX', TRUE), 
(5, 'J', 7, 'FOUR_DX', TRUE), (5, 'J', 8, 'FOUR_DX', TRUE), (5, 'J', 9, 'FOUR_DX', TRUE), 
(5, 'J', 10, 'FOUR_DX', TRUE);

-- Rows K and L: 10 seats per row (20 seats total)
INSERT INTO theater_seats (theater_id, seat_row, seat_number, seat_type, is_active) VALUES
(5, 'K', 1, 'FOUR_DX', TRUE), (5, 'K', 2, 'FOUR_DX', TRUE), (5, 'K', 3, 'FOUR_DX', TRUE), 
(5, 'K', 4, 'FOUR_DX', TRUE), (5, 'K', 5, 'FOUR_DX', TRUE), (5, 'K', 6, 'FOUR_DX', TRUE), 
(5, 'K', 7, 'FOUR_DX', TRUE), (5, 'K', 8, 'FOUR_DX', TRUE), (5, 'K', 9, 'FOUR_DX', TRUE), 
(5, 'K', 10, 'FOUR_DX', TRUE),

(5, 'L', 1, 'FOUR_DX', TRUE), (5, 'L', 2, 'FOUR_DX', TRUE), (5, 'L', 3, 'FOUR_DX', TRUE), 
(5, 'L', 4, 'FOUR_DX', TRUE), (5, 'L', 5, 'FOUR_DX', TRUE), (5, 'L', 6, 'FOUR_DX', TRUE), 
(5, 'L', 7, 'FOUR_DX', TRUE), (5, 'L', 8, 'FOUR_DX', TRUE), (5, 'L', 9, 'FOUR_DX', TRUE), 
(5, 'L', 10, 'FOUR_DX', TRUE);
