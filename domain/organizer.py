from dao.fan_id_card_dao import FanIDCardDAO
from dao.match_dao import MatchDAO
from dao.person_dao import PersonDAO
from dao.ticket_dao import TicketDAO
from domain.person import Person
from domain.seat import Seat
from domain.ticket import SingleTicket


class Organizer(Person):

    def __init__(self, username, first_name, last_name, age):
        super().__init__(username, first_name, last_name, age, "organizer")

    @staticmethod
    def add_match(match):
        new_match_id = MatchDAO.add_match(match)
        match.id = new_match_id
        seats = Seat.get_seats()
        for seat in seats:
            price = 20 * seat.block + 5 * seat.row + 3 * seat.place + 0.99
            ticket = SingleTicket(None, None, price, match, seat)
            TicketDAO.add_ticket(ticket)

    @staticmethod
    def update_match(match):
        MatchDAO.update_match(match)

    @staticmethod
    def delete_match(match_id):
        TicketDAO.delete_tickets_by_match_id(match_id)
        MatchDAO.delete_match(match_id)

    @staticmethod
    def cancel_match(match_id):
        paid_money = TicketDAO.get_paid_money(match_id)
        for card_id, price in paid_money:
            if card_id is not None:
                FanIDCardDAO.increase_balance(card_id, price)
        TicketDAO.delete_tickets_by_match_id(match_id)
        MatchDAO.delete_match(match_id)

    @staticmethod
    def construct(username):
        row = PersonDAO.get_by_id(username)
        return Organizer(row[0], row[2], row[3], row[5])
