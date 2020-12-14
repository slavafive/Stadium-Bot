from dao.match_dao import MatchDAO
from domain.person import Person


class Organizer(Person):

    def __init__(self):
        self.match_dao = MatchDAO()

    def add_match(self, match):
        self.match_dao.add_match(match)
        pass

    def update_match(self, match_id, match):
        pass

    def delete_match(self, match_id):
        pass
