class Match:
    def __init__(self, id, host_team, guest_team, date, organizer, match_type):
        self.id = id
        self.host_team = host_team
        self.guest_team = guest_team
        self.date = date
        self.organizer = organizer
        self.match_type = match_type

    def __str__(self):
        return str(self.id) + ": " + self.host_team + " vs " + self.guest_team + "; Date: " + str(self.date) + " "
