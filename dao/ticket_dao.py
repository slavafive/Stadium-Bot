from dao.dao import DAO
from domain.seat import Seat
from domain.ticket import SingleTicket


class TicketDAO(DAO):

    BLOCKS = 3
    ROWS = 3
    PLACES = 3

    def generate_tickets_for_match(self, match_id):
        for block in range(1, self.BLOCKS + 1):
            for row in range(1, self.ROWS + 1):
                for place in range(1, self.PLACES + 1):
                    price = 18 * block + 4 * row + 0.99
                    self.insert("INSERT INTO tickets (match_id, card_id, block, row, place, price) VALUES ({}, NULL, {}, {}, {}, {})".format(
                        match_id, block, row, place, price)
                    )

    def reserve_ticket(self, ticket_id, fan_id_card):
        self.update("UPDATE tickets SET card_id = {} WHERE id = {}".format(fan_id_card, ticket_id))

    def delete_ticket(self, ticket_id):
        self.delete("DELETE FROM tickets WHERE id = {}".format(ticket_id))

    def return_ticket(self, ticket_id):
        self.update("UPDATE tickets SET card_id = NULL WHERE id = {}".format(ticket_id))

    def get_tickets_by_card_id(self, card_id):
        result = self.select("SELECT * FROM tickets WHERE card_id = {}".format(card_id))
        tickets = []
        for row in result:
            seat = Seat(row[3], row[4], row[5], row[6])
            tickets.append(SingleTicket(row[0], row[2], row[1], seat))
        return tickets

    def remove_tickets_by_card_id(self, card_id):
        self.delete("DELETE FROM tickets WHERE card_id = {}".format(card_id))

    def get_ticket(self, ticket_id):
        result = self.select("SELECT * FROM tickets WHERE id = {}".format(ticket_id))
        row = result[0]
        ticket = SingleTicket(row[0], row[2], row[1], Seat(row[3], row[4], row[5], row[6]))
        return ticket

    def get_ticket_price(self, ticket_id):
        result = self.select("SELECT price FROM tickets WHERE id = {}".format(ticket_id))
        return result[0][0]

    def get_seats_for_match(self, match_id):
        result = self.select("SELECT id, block, row, place, price FROM tickets WHERE match_id = {} AND card_id is NULL".format(match_id))
        tickets_id_and_seats = []
        for row in result:
            seat = Seat(row[1], row[2], row[3], row[4])
            tickets_id_and_seats.append((row[0], seat))
        return tickets_id_and_seats

    def reserve_subscription(self, tickets_id, fan_id_card):
        for ticket_id in tickets_id:
            self.reserve_ticket(ticket_id, fan_id_card)

    def does_ticket_id_exist(self, ticket_id):
        result = self.select("SELECT * FROM tickets WHERE id = '{}'".format(ticket_id))
        return len(result) != 0
