import psycopg2


class HeroDatabase:
    conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="super",
            user="postgres",
            password="")  # TODO Make hidden in config file

    def new_save(self, when, how, who):
        insert_string = 'INSERT INTO super(event_when, event_how, event_who) VALUES(TIMESTAMP %s, %s, %s)'
        cur = self.conn.cursor()
        cur.execute(insert_string, (when, how, who,))
        self.conn.commit()
        self.save_new_person(who)

    def save_new_person(self, who):
        insert_string = 'INSERT INTO people(name) VALUES(%s)'
        cur = self.conn.cursor()
        cur.execute(insert_string, (who,))
        self.conn.commit()

    def inspect(self):
        return self.query("SELECT * FROM super;")

    def get_all_people_from_events(self):
        return self.query("SELECT event_who FROM super;")

    def get_all_people_from_people(self):
        return self.query("SELECT name FROM people;")

    def query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        all_results = cur.fetchall()
        cur.close()
        return all_results

    def main(self):
        self.connect()
        self.inspect()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    hero = HeroDatabase()
    hero.main()
