from dao.person_dao import PersonDAO
from domain.person import Person


class InvalidAgeException(Exception):
    pass


class CustomerAlreadyExistsException(Exception):
    pass


class Cashier(Person):

    def __init__(self, username, first_name, last_name, age):
        super().__init__(username, first_name, last_name, age, role="cashier")
        self.dao = PersonDAO()

    def register_customer(self, customer):
        if customer.age < 12:
            raise InvalidAgeException("The age must be at least 12")
        if self.dao.does_username_exist(customer.username):
            raise CustomerAlreadyExistsException("Customer already exists in the database")
        self.dao.add_person(customer)

    def create_fan_id_card(self, customer):
        pass
