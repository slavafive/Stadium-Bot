import hashlib

import psycopg2

from dao.fan_id_card_dao import FanIDCardDAO
from domain.cashier import Cashier
from domain.customer import Customer
from domain.fan_id_card import FanIDCard
from domain.match import Match
from domain.organizer import Organizer
from domain.ticket import SingleTicket

customer = Customer.construct("mario")
organizer = Organizer.construct("cristiano")
cashier = Cashier.construct("slava")
# match = Match(None, "Dortmund", "Sevilla", "2021-03-10", organizer.username, "quarterfinal")
# organizer.add_match(match)
# new_customer = Customer("alexis", "alexis", "sanchez", 29, None)
# cashier.register(new_customer)

def encrypt_password(password):
    return hashlib.md5(password.encode()).hexdigest()


print(encrypt_password("weston"))
print(encrypt_password("alexis"))
