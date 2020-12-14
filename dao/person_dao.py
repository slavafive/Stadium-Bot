from dao.dao import DAO
import hashlib


class UserExistsError(Exception):
    pass


class PersonDAO(DAO):

    def __init__(self):
        super().__init__()

    def add_person(self, person):
        if self.does_username_exist(person.username):
            raise UserExistsError("User {} already exists in the system".format(person.username))
        self.insert("INSERT INTO person (username, password, first_name, last_name, age, role) VALUES ('{}', '{}', '{}', "
                 "'{}', {}, '{}')".format(
            person.username, self.encrypt_password(person.password), person.first_name, person.last_name,
            person.age, person.role
        ))

    def add_balance(self, username, value):
        self.update("UPDATE person SET balance = balance + {} WHERE username = '{}'".format(value, username))

    def subtract_balance(self, username, value):
        self.add_balance(username, -value)

    def get_balance(self, username):
        result = self.select("SELECT balance FROM person WHERE username = '{}'".format(username))
        return result[0][0]

    def encrypt_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def does_username_exist(self, username):
        result = self.select("SELECT * FROM person WHERE username = '{}'".format(username))
        return len(result) > 0

    def is_password_correct(self, username, password):
        encrypted_password = self.encrypt_password(password)
        result = self.select("SELECT * FROM person WHERE username = '{}' and password = '{}'".format(username, encrypted_password))
        return len(result) != 0

    def get_person(self, username):
        pass
