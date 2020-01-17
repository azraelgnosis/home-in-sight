CREATE TABLE properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zpid INTEGER,
    street TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zipcode INTEGER NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    url TEXT,
    use_code,
    beds INTEGER,
    baths REAL,
    property_area INTEGER,
    lot_area INTEGER,
    year_built INTEGER,
    year_updated INTEGER
)

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    street TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zipcode TEXT NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    type TEXT NOT NULL
)