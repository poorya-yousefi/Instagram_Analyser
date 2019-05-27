import datetime


class AppUser:
    def __init__(self, lastLoginDate: datetime, hasTwoStep: bool,
                 country: str, city: str, phoneNum: str,
                 personalityKeyWords: str, cookie_path: str):
        self.userId = -1
        self.signupDate = None
        self.lastLoginDate = lastLoginDate
        self.hasTwoStep = hasTwoStep
        self.country = country
        self.city = city
        self.phoneNum = phoneNum
        self.personalityKeyWords = personalityKeyWords
        self.cookie_path = cookie_path

    def __str__(self):
        return "<Id: {0} | lastLogin: {1}>".format(self.userId, self.lastLoginDate)
