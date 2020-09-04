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

    def new_save(self, when, how, who):
        insert_string = 'INSERT INTO events(event_when, event_how) VALUES(TIMESTAMP %s, %s)'
        cur = self.conn.cursor()
        cur.execute(insert_string, (when, how,))
        self.conn.commit()
        self.save_new_person(who)

    def save_new_person(self, who):
        insert_string = 'INSERT INTO people(name) VALUES(%s)'
        cur = self.conn.cursor()
        cur.execute(insert_string, (who,))
        self.conn.commit()

    def inspect_all(self):
        return self.query("SELECT * FROM events;")

    def get_all_people_from_people(self):
        return self.query("SELECT name FROM people;")

    def query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        all_results = cur.fetchall()
        cur.close()
        return all_results

    def remove_person_from_database(self, person):
        cur = self.conn.cursor()
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
