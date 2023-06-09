DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_movies;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE user_movies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  movie_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);