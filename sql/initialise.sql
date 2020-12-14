INSERT INTO person (username, first_name, last_name, age, role) VALUES ('mario', 'Mario', 'Martinez', 25, 'customer');
INSERT INTO person (username, first_name, last_name, age, role) VALUES ('fabio', 'Fabio', 'Jackson', 27, 'customer');
INSERT INTO person (username, first_name, last_name, age, role) VALUES ('kylian', 'Kylian', 'Mbappe', 22, 'customer');
INSERT INTO person (username, first_name, last_name, age, role) VALUES ('arthur', 'Arthur', 'Melo', 24, 'customer');
INSERT INTO person (username, first_name, last_name, age, role) VALUES ('slava', 'Vyacheslav', 'Efimov', 21, 'cashier');
INSERT INTO person (username, first_name, last_name, age, role) VALUES ('cristiano', 'Cristiano', 'Ronaldo', 35, 'organizer');
INSERT INTO person (username, first_name, last_name, age, role) VALUES ('lionel', 'Lionel', 'Messi', 32, 'organizer');

INSERT INTO cards (username, expiration_date) VALUES ('mario', '2021-10-10');
INSERT INTO cards (username, expiration_date) VALUES ('fabio', '2022-04-04');
INSERT INTO cards (username, expiration_date) VALUES ('kylian', '2021-12-17');
INSERT INTO cards (username, expiration_date) VALUES ('arthur', '2021-08-25');

INSERT INTO matches (host, guest, match_date, organizer, match_type) VALUES ('Barcelona', 'Juventus', '2020-12-08', 'cristiano', 'group');
INSERT INTO matches (host, guest, match_date, organizer, match_type) VALUES ('Chelsea', 'Sevilla', '2020-12-09', 'cristiano', 'group');
INSERT INTO matches (host, guest, match_date, organizer, match_type) VALUES ('Dortmund', 'Lazio', '2020-11-29', 'cristiano', 'group');
INSERT INTO matches (host, guest, match_date, organizer, match_type) VALUES ('Juventus', 'Chelsea', '2021-01-06', 'cristiano', 'group');
INSERT INTO matches (host, guest, match_date, organizer, match_type) VALUES ('Real Madrid', 'Leipzig', '2020-01-07', 'lionel', 'quarterfinal');
INSERT INTO matches (host, guest, match_date, organizer, match_type) VALUES ('PSG', 'Liverpool', '2020-01-07', 'lionel', 'quarterfinal');

INSERT INTO tickets (match_id, card_id, block, row, place, price) VALUES (1, 3, 1, 1, 1, 35.99);
INSERT INTO tickets (match_id, card_id, block, row, place, price) VALUES (1, 2, 1, 1, 2, 49.99);
INSERT INTO tickets (match_id, card_id, block, row, place, price) VALUES (2, 6, 1, 1, 3, 38.99);
INSERT INTO tickets (match_id, card_id, block, row, place, price) VALUES (2, 6, 1, 2, 1, 45.99);