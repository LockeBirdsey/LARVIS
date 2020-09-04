import psycopg2


class HeroDatabase:
    conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host="postgres",
                database="superhero",
                user="postgres",
                password="password")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # Save a new event into the events table and the person into the people table
    # and link based on the person's generated id
    def new_save(self, when, how, who):
        insert_string = 'INSERT INTO events(event_when, event_how, who_id) VALUES(TIMESTAMP %s, %s, %s)'
        cur = self.conn.cursor()
        person_id = self.save_new_person(who)
        cur.execute(insert_string, (when, how, person_id))
        self.conn.commit()

    def save_new_person(self, who):
        insert_string = 'INSERT INTO people(name) VALUES(%s) RETURNING id;'
        cur = self.conn.cursor()
        cur.execute(insert_string, (who,))
        self.conn.commit()
        return cur.fetchone()[0]

    def get_persons_id(self, who):
        return self.query_with_params('SELECT id FROM people WHERE name = %s', (who,))[0]

    def inspect_all(self):
        return self.query(
            'SELECT * FROM events LEFT OUTER JOIN people ON (events.who_id = people.id) ORDER BY events.event_when;')

    def get_all_people_from_people(self):
        return self.query("SELECT name, id FROM people ORDER BY id;")

    def query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        all_results = cur.fetchall()
        cur.close()
        return all_results

    def query_with_params(self, query, params):
        cur = self.conn.cursor()
        cur.execute(query, params)
        all_results = cur.fetchall()
        cur.close()
        return all_results

    def remove_person_from_database(self, person):
        cur = self.conn.cursor()
        person_id = self.get_persons_id(person)
        cur.execute("UPDATE events SET who_id = NULL WHERE who_id = %s", (person_id,))
        cur.execute("DELETE FROM people WHERE name = %s", (person,))
        self.conn.commit()

    def rename_person_in_database(self, orig_name, new_name):
        cur = self.conn.cursor()
        cur.execute("UPDATE people SET name = %s WHERE name = %s", (new_name, orig_name,))
        self.conn.commit()

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
