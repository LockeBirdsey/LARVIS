import psycopg2
from datetime import datetime


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

    def inspect(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM super;")
        db_version = cur.fetchall()
        print(db_version)
        cur.close()

    def main(self):
        self.connect()
        self.inspect()


if __name__ == '__main__':
    hero = HeroDatabase()
    hero.main()
