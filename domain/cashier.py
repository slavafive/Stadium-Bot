from dao.person_dao import PersonDAO
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

    @staticmethod
    def block_fan_id_card(customer):
        customer.fan_id_card.block()

    @staticmethod
    def unblock_fan_id_card(customer):
        customer.fan_id_card.unblock()
