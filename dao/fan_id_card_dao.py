from dao.dao import DAO
from dao.person_dao import UsernameNotFoundError


class FanIDCardNotFoundError(Exception):
    pass


class FanIDCardDAO(DAO):

    @staticmethod
    def get_card_by_id(card_id):
        result = DAO.select("SELECT * FROM cards WHERE id = {}".format(card_id))
        if len(result) == 0:
            raise FanIDCardNotFoundError("Fan ID Card {} does not exist".format(card_id))
        return result[0]

    @staticmethod
    def get_card_by_username(username):
        result = DAO.select("SELECT * FROM cards WHERE username = '{}'".format(username))
        if len(result) == 0:
            raise UsernameNotFoundError("Username {} was not found in the system".format(username))
        return result[0]

    @staticmethod
    def increase_balance(card_id, value):
        DAO.update("UPDATE cards SET balance = balance + {} WHERE id = {}".format(value, card_id))

    @staticmethod
    def reduce_balance(card_id, value):
        FanIDCardDAO.increase_balance(card_id, -value)

    @staticmethod
    def does_exist(card_id):
        result = DAO.select("SELECT * FROM cards WHERE id = {}".format(card_id))
        return len(result) > 0

    @staticmethod
    def insert(card):
        DAO.insert("INSERT INTO cards (username, expiration_date, balance, is_blocked) VALUES ('{}', '{}', {}, '{}')".
            format(card.username, card.expiration_date, card.balance, card.is_blocked))

    @staticmethod
    def update(card):
        DAO.update("UPDATE cards SET username = '{}', expiration_date = '{}', balance = {}, is_blocked = '{}' WHERE id = {}".
                   format(card.username, card.expiration_date, card.balance, card.is_blocked, card.id))

    @staticmethod
    def save(card):
        if FanIDCardDAO.does_exist(card.id):
            FanIDCardDAO.update(card)
        else:
            FanIDCardDAO.insert(card)

    @staticmethod
    def get_max_card_id():
        max_card_id = DAO.select("SELECT MAX(id) FROM cards")[0][0]
        return max_card_id
