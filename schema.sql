drop table if exists users;
	CREATE TABLE users (
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		username TEXT NOT NULL,
		hash TEXT NOT NULL
);
