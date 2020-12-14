from domain.person import Person


class Customer(Person):
    def __init__(self, username, first_name, last_name, age, fan_id_card, balance=0, tickets=[]):
        super().__init__(username, first_name, last_name, age, "customer")
        self.fan_id_card = fan_id_card
        self.balance = balance
        self.tickets = tickets
