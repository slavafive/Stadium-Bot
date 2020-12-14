import psycopg2


class DAO:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            database="stadium",
            user="slava",
            password="123"
        )
        self.cur = self.con.cursor()

    def select(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def modify(self, query):
        self.cur.execute(query)
        self.con.commit()

    def insert(self, query):
        self.modify(query)

    def update(self, query):
        self.modify(query)

    def delete(self, query):
        self.modify(query)

    def __del__(self):
        self.cur.close()
