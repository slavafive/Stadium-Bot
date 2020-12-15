CREATE TABLE person (
    username varchar(255) PRIMARY KEY,
    password varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    role varchar(255),
    age int
);

CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    username varchar(255) REFERENCES person(username),
    expiration_date date,
    balance real DEFAULT 0,
    is_blocked boolean DEFAULT FALSE
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    host varchar(255),
    guest varchar(255),
    match_date date,
    organizer varchar(255) REFERENCES person(username),
    match_type varchar(255)
);

CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    card_id int REFERENCES cards(id),
    price real,
    match_id int REFERENCES matches(id),
    block int,
    row int,
    place int
);