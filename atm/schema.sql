DROP TABLE IF EXISTS account;

CREATE TABLE account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  card_number TEXT UNIQUE NOT NULL,
  pin_number TEXT NOT NULL,
  balance INTEGER DEFAULT 0
);