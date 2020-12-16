from dao.ticket_dao import TicketDAO
from domain.fan_id_card import FanIDCard
from domain.match import Match
from domain.seat import Seat


class TicketDoesNotExistError(Exception):
    pass


class Ticket:
    def __init__(self, ticket_id, fan_id_card, price):
        self.id = ticket_id
        self.fan_id_card = fan_id_card
        self.price = price


class SingleTicket(Ticket):
    def __init__(self, ticket_id, fan_id_card, price, match, seat):
        super().__init__(ticket_id, fan_id_card, price)
        self.match = match
        self.seat = seat

    def __str__(self):
        return "Ticket ID: {}\n{}\n".format(self.id, self.match) + "Seat: " + str(self.seat)

    @staticmethod
    def construct(ticket_id):
        if not TicketDAO.does_exist(ticket_id):
            raise TicketDoesNotExistError()
        row = TicketDAO.get_by_id(ticket_id)
        if row[1] is None:
            fan_id_card = None
        else:
            card_id = int(row[1])
            fan_id_card = FanIDCard.construct(card_id)
        match_id = int(row[3])
        match = Match.construct(match_id)
        seat = Seat(row[4], row[5], row[6])
        return SingleTicket(row[0], fan_id_card, row[2], match, seat)


class SeasonTicket(Ticket):
    def __init__(self, ticket_id, fan_id_card, price, tickets):
        super().__init__(ticket_id, fan_id_card, price)
        self.tickets = tickets

