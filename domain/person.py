import random


class Person:
    def __init__(self, username, first_name, last_name, age, role):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.role = role
        self.password = self.generate_password()

    def generate_password(self):
        length = 8
        str = "abcdefghijklmnopqrstuvwxyz0123456789"
        allowed_characters = []
        for symbol in str:
            allowed_characters.append(symbol)
        password = []
        for i in range(length):
            password.append(allowed_characters[random.randint(0, len(allowed_characters) - 1)])
        return "".join(password)
