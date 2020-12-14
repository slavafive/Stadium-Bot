from dao.dao import DAO
from domain.fan_id_card import FanIDCard


class FanIDCardDAO(DAO):

    def add_fan_id_card(self, card):
        self.insert("INSERT INTO cards (id, username, expiration_date, is_blocked) VALUES ({}, '{}', '{}', '{}')"
                    .format(card.id, card.username, card.expiration_date, card.is_blocked))

    def block(self, card_id):
        self.update("UPDATE cards SET is_blocked = true WHERE id = {}".format(card_id))

    def unblock(self, card_id):
        self.update("UPDATE cards SET is_blocked = false WHERE id = {}".format(card_id))

    def get_fan_id_card(self, card_id):
        result = self.select("SELECT * FROM cards WHERE id = {}".format(card_id))
        if len(result) == 0:
            return None
        row = result[0]
        return FanIDCard(row[0], row[1], row[3], row[2])

    def get_username_by_fan_id(self, card_id):
        result = self.select("SELECT username FROM cards WHERE id = {}".format(card_id))
        return result[0][0]

    def get_card_id_by_username(self, username):
        result = self.select("SELECT id FROM cards WHERE username = '{}'".format(username))
        return result[0][0]

    def does_fan_id_card_exist(self, card_id):
        return True

    def get_max_card_id(self):
        result = self.select("SELECT max(id) FROM cards")
        return result[0][0]

    def generate_next_id(self):
        return int(self.get_max_card_id()) + 1

    def save(self, fan_id_card):
        pass