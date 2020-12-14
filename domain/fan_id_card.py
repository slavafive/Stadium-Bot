import datetime

class FanIDCard:

    EXPIRATION_PERIOD_IN_YEARS = 2

    def __init__(self, id, username, is_blocked, expiration_date=None):
        self.id = id
        self.username = username
        self.expiration_date = self.get_expiration_date() if expiration_date is None else expiration_date
        self.is_blocked = is_blocked

    def get_expiration_date(self):
        now = datetime.datetime.now()
        year = str(now.year + self.EXPIRATION_PERIOD_IN_YEARS)
        month = str(now.month) if len(str(now.month)) == 2 else "0" + str(now.month)
        day = str(now.day) if len(str(now.day)) == 2 else "0" + str(now.day)
        return year + "-" + month + "-" + day
