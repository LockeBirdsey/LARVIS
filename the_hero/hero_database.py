import psycopg2


class HeroDatabase:
    conn = None

    # Attempt to connect to the database
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host="postgres",
                database="superhero",
                user="postgres",
                password="password")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # Executes a simple query and returns all results
    def query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        all_results = cur.fetchall()
        cur.close()
        return all_results

    # Executes a query with additional parameters and returns all results
    def query_with_params(self, query, params):
        cur = self.conn.cursor()
        cur.execute(query, params)
        all_results = cur.fetchall()
        cur.close()
        return all_results

    # Save a new event into the events table and the person into the people table
    # and link based on the person's generated id
    def new_save(self, when, how, who):
        insert_string = 'INSERT INTO events(event_when, event_how, who_id) VALUES(TIMESTAMP %s, %s, %s)'
        cur = self.conn.cursor()
        person_id = self.save_new_person(who)
        cur.execute(insert_string, (when, how, person_id))
        self.conn.commit()

    # Save a new person into the people table and return their id
    def save_new_person(self, who):
        insert_string = 'INSERT INTO people(name) VALUES(%s) RETURNING id;'
        cur = self.conn.cursor()
        cur.execute(insert_string, (who,))
        self.conn.commit()
        return cur.fetchone()[0]

    # Returns all events order by when they were performed
    def inspect_all(self):
        return self.query(
            'SELECT * FROM events LEFT OUTER JOIN people ON (events.who_id = people.id) ORDER BY events.event_when;')

    # Returns all people ordered by their id number
    def get_all_people(self):
        return self.query("SELECT name, id FROM people ORDER BY id;")

    # Removes a person from the database using their id
    def remove_person_with_id(self, person_id):
        cur = self.conn.cursor()
        cur.execute("UPDATE events SET who_id = NULL WHERE who_id = %s", (person_id,))
        cur.execute("DELETE FROM people WHERE id = %s", (person_id,))
        self.conn.commit()

    # Renames a person
    def rename_person(self, person_id, new_name):
        cur = self.conn.cursor()
        cur.execute("UPDATE people SET name = %s WHERE id = %s", (new_name, person_id,))
        self.conn.commit()

    # Close DB connection
    def close(self):
        if self.conn is not None:
            self.conn.close()

    # For offline testing purposes
    def test_db(self):
        self.connect()
        self.inspect_all()


if __name__ == '__main__':
    hero = HeroDatabase()
    hero.test_db()
