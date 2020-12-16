from dao.match_dao import MatchDAO


class MatchDoesNotExistError(Exception):
    pass


class Match:
    def __init__(self, id, host_team, guest_team, date, organizer, match_type):
        self.id = id
        self.host_team = host_team
        self.guest_team = guest_team
        self.date = date
        self.organizer = organizer
        self.match_type = match_type

    def __str__(self):
        return "----- Match {} -----\n{} vs {}\n{} Stage\nDate: {}".format(self.id, self.host_team, self.guest_team, self.match_type, self.date)

    @staticmethod
    def construct(match_id):
        if not MatchDAO.does_exist(match_id):
            raise MatchDoesNotExistError()
        row = MatchDAO.get_by_id(match_id)
        return Match(row[0], row[1], row[2], row[3], row[4], row[5])

    def save(self):
        MatchDAO.update_match(self)
