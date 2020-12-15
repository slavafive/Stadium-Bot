import psycopg2

from dao.fan_id_card_dao import FanIDCardDAO
from domain.customer import Customer
from domain.fan_id_card import FanIDCard
from domain.ticket import SingleTicket

customer = Customer.construct("mario")
a = 9
