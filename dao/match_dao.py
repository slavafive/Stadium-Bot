from dao.dao import DAO
from domain.match import Match


class MatchDAO(DAO):

    def add_match(self, match):
        self.insert("INSERT INTO matches (host, guest, match_date, organizer, match_type) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            match.host_team, match.guest_team, match.date, match.organizer, match.match_type
        ))

    def update_match(self, match):
        self.update("UPDATE matches SET host = '{}', guest = '{}', match_date = '{}', organizer = '{}', match_type = '{}' WHERE id = {}".format(
            match.host_team, match.guest_team, match.date, match.organizer, match.match_type, match.id
        ))

    def delete_match(self, match_id):
        self.delete("DELETE FROM matches WHERE id = {}".format(match_id))

    def get_match(self, match_id):
        return self.select("SELECT * FROM matches WHERE id = {}".format(match_id))

    def get_matches(self):
        result = self.select("SELECT * FROM matches")
        matches = []
        for row in result:
            matches.append(Match(*row))
        return matches
