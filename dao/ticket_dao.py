from dao.dao import DAO


class TicketDAO(DAO):

    @staticmethod
    def add_ticket(ticket):
        seat = ticket.seat
        DAO.insert("INSERT INTO tickets (price, match_id, block, row, place) VALUES ({}, {}, {}, {}, {})"
                   .format(ticket.price, ticket.match.id, seat.block, seat.row, seat.place))

    @staticmethod
    def get_ticket_by_id(ticket_id):
        return DAO.select("SELECT * FROM tickets WHERE id = {}".format(ticket_id))[0]

    @staticmethod
    def get_tickets_id_by_card_id(card_id):
        return DAO.select("SELECT id FROM tickets WHERE card_id = {} ORDER BY id".format(card_id))

    @staticmethod
    def get_available_tickets_id_and_seats_and_price(match_id):
        return DAO.select("SELECT id, block, row, place, price FROM tickets WHERE match_id = {} AND card_id is NULL ORDER BY id".format(match_id))

    @staticmethod
    def reserve_ticket(ticket_id, card_id):
        DAO.update("UPDATE tickets SET card_id = {} WHERE id = {}".format(card_id, ticket_id))

    @staticmethod
    def return_ticket(ticket_id):
        DAO.update("UPDATE tickets SET card_id = NULL WHERE id = {}".format(ticket_id))

    @staticmethod
    def delete_tickets_by_match_id(match_id):
        DAO.delete("DELETE FROM tickets WHERE match_id = {}".format(match_id))

    @staticmethod
    def get_paid_money(match_id):
        result = DAO.select("SELECT card_id, price FROM tickets WHERE match_id = {}".format(match_id))
        return result

    @staticmethod
    def does_exist(ticket_id):
        result = DAO.select("SELECT * FROM tickets WHERE id = {}".format(ticket_id))
        return len(result) > 0
