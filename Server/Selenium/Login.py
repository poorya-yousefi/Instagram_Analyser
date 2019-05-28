from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException


class Login:

    def __init__(self, username, password):

        # initializing the username and password to login and do the other things
        self.userName = username
        self.password = password
        self.code = None

        # Return values
        self.incorrectPass = "Incorrect Password"
        self.successLogin = "login Successfully"
        self.incorrectCode = "Incorrect verification code"

        self.sleep = 4

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        self.driver = webdriver.Firefox(
            executable_path=r'C:\Users\erfan\.wdm\geckodriver\v0.24.0\win64\geckodriver.exe',
            firefox_profile=firefox_profile)
        self.letter = {
            "driver": self.driver,
            "result": None
        }

    # closing a browser after finishing
    def close_browser(self):
        self.driver.close()

    # login to special page
    def login(self):

        self.driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        time.sleep(self.sleep)
        user_name_elem = self.driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.userName)
        password_elem = self.driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(self.sleep)

        while True:
            try:
                self.driver.find_element_by_xpath("//p[@id='slfErrorAlert']")
                self.letter["result"] = self.incorrectPass
                self.driver.close()
                return self.letter
            except NoSuchElementException:
                break

        while True:
            try:
                self.driver.find_element_by_xpath("//input[@name='verificationCode']")
                self.letter["result"] = "two step is enable"
                self.driver.close()
                return self.letter

            except NoSuchElementException:
                break

        # saving the cookies for this user
        save_cookies(self.userName, self.driver.get_cookies())
        self.driver.close()
        self.letter["result"] = self.successLogin
        return self.letter

    # two step verification code for login to instagram
    def two_step(self, code):
        passsword_vry = self.driver.find_element_by_xpath("//input[@name='verificationCode']")
        passsword_vry.clear()
        passsword_vry.send_keys(code)
        passsword_vry.send_keys(Keys.RETURN)
        time.sleep(self.sleep)
        while True:
            try:
                self.driver.find_element_by_xpath("//p[@id='twoFactorErrorAlert']")
                self.letter["result"] = self.incorrectCode
                return self.letter
            except NoSuchElementException:
                print("such kind of elements didn't find")
                break

        return self.successLogin


# A function to save cookies
def save_cookies(username, cookies):

        file = open("../../inf/cookies/" + username + ".data", "w+")
        for cookie in cookies:
            file.write(str(cookie) + '\n')
