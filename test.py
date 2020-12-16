import hashlib
import re

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

# def encrypt_password(password):
#     return hashlib.md5(password.encode()).hexdigest()
#
#
# print(encrypt_password("mario"))

date="13-11-2017"

x=re.search("^([1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|)20[0-9][0-9]$",date)

x.group()