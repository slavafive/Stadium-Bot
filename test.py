import psycopg2

from dao.fan_id_card_dao import FanIDCardDAO
from domain.customer import Customer
from domain.fan_id_card import FanIDCard
from domain.match import Match
from domain.organizer import Organizer
from domain.ticket import SingleTicket

customer = Customer.construct("mario")
a = 9
organizer = Organizer.construct("cristiano")
b = 8
match = Match(None, "Dortmund", "Sevilla", "2021-03-10", organizer.username, "quarterfinal")
organizer.add_match(match)
