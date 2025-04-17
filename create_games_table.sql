CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rank INTEGER,
    rating REAL,
    year_published INTEGER,
    min_players INTEGER,
    max_players INTEGER
);