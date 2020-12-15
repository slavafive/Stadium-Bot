from dao.fan_id_card_dao import FanIDCardDAO
from dao.match_dao import MatchDAO
from dao.person_dao import PersonDAO
from dao.ticket_dao import TicketDAO
from domain.person import Person


class Organizer(Person):

    def __init__(self, username, first_name, last_name, age):
        super().__init__(username, first_name, last_name, age, "organizer")

    @staticmethod
    def add_match(match):
        MatchDAO.add_match(match)

    @staticmethod
    def update_match(match):
        MatchDAO.update_match(match)

    @staticmethod
    def delete_match(match_id):
        MatchDAO.delete_match(match_id)

    @staticmethod
    def cancel_match(match_id):
        paid_money = TicketDAO.get_paid_money(match_id)
        for card_id, price in paid_money:
            FanIDCardDAO.increase_balance(card_id, price)
        TicketDAO.delete_tickets_by_match_id(match_id)
        MatchDAO.delete_match(match_id)

    @staticmethod
    def construct(username):
        row = PersonDAO.get_person_by_username(username)
        return Organizer(row[0], row[2], row[3], row[5])
