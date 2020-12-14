class Ticket:
    def __init__(self, ticket_id, card_id):
        self.id = ticket_id
        self.card_id = card_id


    def get_information(self):
        pass


class SingleTicket(Ticket):
    def __init__(self, ticket_id, card_id, match_id, seat):
        super().__init__(ticket_id, card_id)
        self.match_id = match_id
        self.seat = seat

    def __str__(self):
        return "ID: {}, Match ID: {}, ".format(self.id, self.match_id) + str(self.seat)


class SeasonTicket(Ticket):
    def __init__(self, ticket_id, customer, tickets=[]):
        super().__init__(ticket_id, customer)
        self.tickets = tickets

