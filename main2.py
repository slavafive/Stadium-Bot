import psycopg2

from dao.match_dao import MatchDAO
from dao.ticket_dao import TicketDAO

con = psycopg2.connect(
    host="localhost",
    database="stadium",
    user="slava",
    password="123"
)

match_dao = MatchDAO()
ticket_dao = TicketDAO()
ticket_dao.get_seats_for_match(2)

# cur = con.cursor()
# query = "SELECT * FROM tickets"
# cur.execute(query)
# rows = cur.fetchall()
# print(rows)

# cur.close()
