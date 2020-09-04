CREATE TABLE events(
id serial PRIMARY KEY,
event_when TIMESTAMP NOT NULL,
event_how VARCHAR(5000));

CREATE TABLE people(
id serial PRIMARY KEY,
name VARCHAR(80) NOT NULL);