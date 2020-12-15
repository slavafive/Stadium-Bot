from dao.dao import DAO


class MatchDAO(DAO):

    @staticmethod
    def add_match(match):
        DAO.insert("INSERT INTO matches (host, guest, match_date, organizer, match_type) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            match.host_team, match.guest_team, match.date, match.organizer, match.match_type
        ))
        return MatchDAO.get_max_match_id()

    @staticmethod
    def update_match(match):
        DAO.update("UPDATE matches SET host = '{}', guest = '{}', match_date = '{}', organizer = '{}', match_type = '{}' WHERE id = {}".format(
            match.host_team, match.guest_team, match.date, match.organizer, match.match_type, match.id
        ))

    @staticmethod
    def delete_match(match_id):
        DAO.delete("DELETE FROM matches WHERE id = {}".format(match_id))

    @staticmethod
    def get_match_by_id(match_id):
        return DAO.select("SELECT * FROM matches WHERE id = {}".format(match_id))[0]

    @staticmethod
    def get_max_match_id():
        max_match_id = DAO.select("SELECT MAX(id) FROM matches")[0][0]
        return max_match_id

    @staticmethod
    def get_matches():
        return DAO.select("SELECT * FROM matches ORDER BY id")
