import psycopg2


class DAO:
    con = psycopg2.connect(
            host="localhost",
            database="stadium",
            user="slava",
            password="123"
        )
    cur = con.cursor()

    @staticmethod
    def select(query):
        DAO.cur.execute(query)
        return DAO.cur.fetchall()

    @staticmethod
    def modify(query):
        DAO.cur.execute(query)
        DAO.con.commit()

    @staticmethod
    def insert(query):
        DAO.modify(query)

    @staticmethod
    def update(query):
        DAO.modify(query)

    @staticmethod
    def delete(query):
        DAO.modify(query)

    def __del__(self):
        self.cur.close()
