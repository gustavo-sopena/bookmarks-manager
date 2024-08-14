-- author: Gustavo Sopena
-- date started: 2024-08-10 at 2228

DROP TABLE IF EXISTS bm_url;

CREATE TABLE bm_url (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date_added DATETIME NOT NULL,
  url_text TEXT UNIQUE NOT NULL,
  contains_file INTEGER NOT NULL
);
