import datetime


class AppUser:
    def __init__(self, last_login_date: datetime, has_two_step: bool,
                 country: str, city: str, phone_num: str,
                 personality_key_words: str, cookie_path: str):
        self.userId = -1
        self.signupDate = None
        self.lastLoginDate = last_login_date
        self.hasTwoStep = has_two_step
        self.country = country
        self.city = city
        self.phoneNum = phone_num
        self.personalityKeyWords = personality_key_words
        self.cookie_path = cookie_path

    def __str__(self):  # TODO
        return "<Id: {0} | lastLogin: {1}>".format(self.userId, self.lastLoginDate)


class CommercialUser(AppUser):
    def __init__(self, last_login_date: datetime, has_two_step: bool,
                 country: str, city: str, phone_num: str,
                 personality_key_words: str, cookie_path: str, company_name: str, activity: str):
        AppUser.__init__(self, last_login_date, has_two_step, country, city, phone_num, personality_key_words,
                         cookie_path)
        self.companyName = company_name
        self.activity = activity
