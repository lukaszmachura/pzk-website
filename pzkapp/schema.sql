DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS club;

CREATE TABLE club (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    www TEXT,
    fb TEXT,
    abbrev TEXT,
    FOREIGN KEY (leader_id) REFERENCES member (id)
);

CREATE TABLE member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  kendo_grade TEXT,
  iaido_grade TEXT,
  jodo_grade TEXT,
  kendo_licence TEXT,
  iaido_licence TEXT,
  jodo_licence TEXT
);
