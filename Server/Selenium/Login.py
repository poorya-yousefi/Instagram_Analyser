from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

class Login:

    def __init__(self, userName, password):

        # initializing the username and password to login and do the other things
        self.userName = userName
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

        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        time.sleep(self.sleep)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.userName)
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(self.sleep)

        while True:
            try:
                driver.find_element_by_xpath("//p[@id='slfErrorAlert']")
                self.letter["result"] = self.incorrectPass
                return self.letter
            except NoSuchElementException:
                break

        while True:
            try:
                driver.find_element_by_xpath("//input[@name='verificationCode']")
                self.letter["result"] = "two step is enable"
                return self.letter

            except NoSuchElementException:
                break

        self.letter["result"] = self.successLogin
        return self.letter

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

    # Getting the followers list of username id
    # def get_followers_list(self, username):
    #
    #     driver = self.driver
    #     driver.get("https://www.instagram.com/" + username + "/")
    #     time.sleep(self.sleep)
    #
    #
    #     return ""

    def get_followers_list(self, pagename, connections):
        followers = ""
        sleep = 5
        driver = self.driver

        try:
            driver.get("https://www.instagram.com/" + pagename + "/")
            time.sleep(sleep)
            allfoll = (
                driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"))
            allfoll = allfoll.get_attribute('title')
            allfoll = allfoll.replace(',', '')
            allfoll = int(allfoll)

            if connections == "followers":
                followers_button = driver.find_element_by_xpath(
                    "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a")
            elif connections == "following":
                followers_button = driver.find_element_by_xpath(
                    "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a")

            followers_button.click()
            time.sleep(sleep)
            driver.implicitly_wait(2)
            dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]')
            driver.implicitly_wait(2)
            time.sleep(sleep)
            s = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div")
            time.sleep(sleep)
            s.location_once_scrolled_into_view
            time.sleep(sleep)
            nim = 0
            SCROLL_PAUSE_TIME = 1.2
            # Get scroll height
            last_height = driver.execute_script("return arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            # userslist = []
            cc = 0
            userslistget = driver.find_elements_by_xpath("//div[@class='d7ByH']/a")

            while cc <= 4:
                if len(userslistget) <= allfoll - 3:
                    while True:
                        # Scroll down to bottom
                        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                        # Wait to load page
                        time.sleep(SCROLL_PAUSE_TIME)

                        # Calculate new scroll height and compare with last scroll height
                        new_height = driver.execute_script("return arguments[0].scrollTop = arguments[0].scrollHeight",
                                                           dialog)
                        if new_height == last_height:
                            break
                        last_height = new_height
                        nim = nim + 1
                        print(nim)

                    userslistget = driver.find_elements_by_xpath("//div[@class='d7ByH']/a")
                    print("userlest len", len(userslistget))
                    cc = cc + 1
                else:
                    break

            userslistget = driver.find_elements_by_xpath("//div[@class='d7ByH']/a")
            followers = followers + "page name is:" + "\n" + pagename + "\n"
            if len(userslistget) <= allfoll - 5:
                print("broken file")
                followers = followers + "broken file" + "\n"
            for user in userslistget:
                print(user.get_attribute("title"))
                followers = followers + str(user.get_attribute("title")) + "\n"
            return followers

        except NoSuchElementException:
            pass
