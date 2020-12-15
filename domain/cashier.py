from dao.person_dao import PersonDAO
from domain.fan_id_card import FanIDCard
from domain.person import Person


class InvalidAgeError(Exception):
    pass


class CustomerAlreadyExistsException(Exception):
    pass


class Cashier(Person):

    def __init__(self, username, first_name, last_name, age):
        super().__init__(username, first_name, last_name, age, role="cashier")

    def register(self, person):
        PersonDAO.register(person, self.username)
        self.create_fan_id(person.username)

    def create_fan_id(self, username):
        FanIDCard.create(username)

    @staticmethod
    def block_fan_id_card(customer):
        customer.fan_id_card.block()

    @staticmethod
    def unblock_fan_id_card(customer):
        customer.fan_id_card.unblock()

    @staticmethod
    def construct(username):
        row = PersonDAO.get_person_by_username(username)
        return Cashier(row[0], row[2], row[3], row[5])
