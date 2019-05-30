import datetime


class AppUser:
    def __init__(self, last_login_date: datetime, has_two_step: bool,
                 country: str, city: str, phone_num: str,
                 personality_key_words: str, cookie_path: str, js_path: str):
        self.userId = -1
        self.signupDate = None
        self.lastLoginDate = last_login_date
        self.hasTwoStep = has_two_step
        self.country = country
        self.city = city
        self.phoneNum = phone_num
        self.personalityKeyWords = personality_key_words
        self.cookie_path = cookie_path
        self.js_path = js_path

    def __str__(self):
        return "<Id: {0} | signupDate: {1} | lastLoginDate: {2} | hasTwoStep: {3} | country: {4} | city: {5} | " \
               "phoneNum: {6} | personalityKeyWords: {7} | cookie_path: {8} | js_path: {9}>".format \
            (self.userId, self.signupDate, self.lastLoginDate, self.hasTwoStep, self.country, self.city, self.phoneNum,
             self.personalityKeyWords, self.cookie_path, self.js_path)


class CommercialUser(AppUser):
    def __init__(self, last_login_date: datetime, has_two_step: bool,
                 country: str, city: str, phone_num: str,
                 personality_key_words: str, cookie_path: str, js_path: str, company_name: str, activity: str):
        AppUser.__init__(self, last_login_date, has_two_step, country, city, phone_num, personality_key_words,
                         cookie_path, js_path)
        self.companyName = company_name
        self.activity = activity
