DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS club;
DROP TABLE IF EXISTS event;

CREATE TABLE club (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    abbrev TEXT,
    email TEXT UNIQUE, /*official club email*/
    address TEXT,
    phone TEXT,
    www TEXT,
    fb TEXT,
    licence TEXT,
    magic TEXT UNIQUE NOT NULL  /*unique number for registration*/
);

CREATE TABLE member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  first_name TEXT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  club TEXT NOT NULL,
  club_id UNSIGNED SMALLINT NOT NULL,
  pesel CHAR(11) NOT NULL DEFAULT "01010100000",
  address TEXT,
  phone TEXT,
  student BOOLEAN DEFAULT 0,
  kendo_grade TEXT,
  iaido_grade TEXT,
  jodo_grade TEXT,
  kendo_licence TEXT,
  iaido_licence TEXT,
  jodo_licence TEXT,
  events TEXT,
  past_events TEXT,
  pzk TEXT,  -- funkcja w PZK
  kendo_instructor BOOLEAN DEFAULT 0,
  iaido_instructor BOOLEAN DEFAULT 0,
  jodo_instructor BOOLEAN DEFAULT 0,
  kendo_coach BOOLEAN DEFAULT 0,
  iaido_coach BOOLEAN DEFAULT 0,
  jodo_coach BOOLEAN DEFAULT 0,
  delegate BOOLEAN DEFAULT 0,
  FOREIGN KEY (club_id) REFERENCES club (id)
);

CREATE TABLE event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    date DATE,  /*YYYY-MM-DD*/
    art TEXT,  /*k, i, j, ki, kj, ij, kij*/
    host_id UNSIGNED SMALLINT NOT NULL DEFAULT 0,
    venue TEXT,
    www TEXT,
    fb TEXT,
    price UNSIGNED SMALLINT,
    euro26 UNSIGNED SMALLINT,
    promo UNSIGNED SMALLINT,
    promo_date DATE,  /*YYYY-MM-DD*/
    active BOOLEAN DEFAULT 1;
    FOREIGN KEY (host_id) REFERENCES club (id)
);
