DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS club;

CREATE TABLE club (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    magic TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    address TEXT,
    phone TEXT,
    www TEXT,
    fb TEXT,
    abbrev TEXT
);

CREATE TABLE member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  club TEXT NOT NULL,
  club_id INTEGER NOT NULL,
  name TEXT,
  first_name TEXT,
  kendo_grade TEXT,
  iaido_grade TEXT,
  jodo_grade TEXT,
  kendo_licence TEXT,
  iaido_licence TEXT,
  jodo_licence TEXT,
  FOREIGN KEY (club_id) REFERENCES club (id)
);
