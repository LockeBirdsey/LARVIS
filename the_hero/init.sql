CREATE TABLE people(
id serial PRIMARY KEY,
name TEXT NOT NULL);

CREATE TABLE events(
id serial PRIMARY KEY,
event_when TIMESTAMP NOT NULL,
event_how TEXT NOT NULL,
who_id INTEGER,
FOREIGN KEY(who_id) REFERENCES people(id));