from dao.person_dao import PersonDAO
from domain.fan_id_card import FanIDCard
from domain.person import Person


class InvalidAgeError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class IncorrectInputFormat(Exception):
    pass


class Cashier(Person):

    MAX_LENGTH = 20

    def __init__(self, username, first_name, last_name, age):
        super().__init__(username, first_name, last_name, age, role="cashier")

    def register(self, person):
        if len(person.username) > self.MAX_LENGTH or len(person.first_name) > self.MAX_LENGTH or len(person.last_name) > self.MAX_LENGTH or person.age > 99:
            raise IncorrectInputFormat("The input does not correspond to system format. "
                                       "The age must be in range from 12 to 99 and other fields must not exceed the length of {} symbols".format(self.MAX_LENGTH))
        if PersonDAO.does_exist(person.username):
            raise UserAlreadyExistsError("User already exists in the system")
        PersonDAO.register(person, self.username)
        person.fan_id_card = self.create_fan_id(person.username)

    def create_fan_id(self, username):
        return FanIDCard.create(username)

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
