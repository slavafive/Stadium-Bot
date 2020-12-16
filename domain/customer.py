from dao.person_dao import PersonDAO
from domain.fan_id_card import FanIDCard
from domain.person import Person


class TicketDoesNotBelongToCustomerError(Exception):
    pass


class CustomerDoesNotExistError(Exception):
    pass


class Customer(Person):

    def __init__(self, username, first_name, last_name, age, fan_id_card):
        super().__init__(username, first_name, last_name, age, "customer")
        self.fan_id_card = fan_id_card

    def buy_ticket(self, ticket):
        self.fan_id_card.reserve_ticket(ticket)

    def return_ticket(self, ticket):
        if ticket.fan_id_card is None or self.fan_id_card.id != ticket.fan_id_card.id:
            raise TicketDoesNotBelongToCustomerError()
        self.fan_id_card.return_ticket(ticket)

    def increase_balance(self, value):
        self.fan_id_card.increase_balance(value)

    def is_blocked(self):
        return self.fan_id_card.is_blocked

    @staticmethod
    def construct(username):
        if not PersonDAO.does_exist(username) or PersonDAO.get_role_by_username(username) != "customer":
            raise CustomerDoesNotExistError()
        row = PersonDAO.get_person_by_username(username)
        card = FanIDCard.construct_by_username(username)
        return Customer(row[0], row[2], row[3], row[5], card)
