from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from Mutual import mutual
import requests
import re


class Login:

    def __init__(self, username, password):

        # initializing the username and password to login and do the other things
        self.userName = username
        self.password = password
        self.code = None

        self.sleep = 4

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        self.driver = webdriver.Firefox(
            executable_path=r'C:\Users\erfan\.wdm\geckodriver\v0.24.0\win64\geckodriver.exe',
            firefox_profile=firefox_profile)
        self.letter = {
           "response": ""
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
                self.letter["response"] = mutual.incorrectPass
                self.driver.close()
                return self.letter
            except NoSuchElementException:
                break

        while True:
            try:
                self.driver.find_element_by_xpath("//input[@name='verificationCode']")
                self.letter["response"] = mutual.twoStepEn
                self.driver.close()
                return self.letter

            except NoSuchElementException:
                break

        # saving the cookies for this user
        save_cookies(self.userName, self.driver.get_cookies())
        self.driver.close()
        self.letter["response"] = mutual.successLogin
        return self.letter

    # two step verification code for login to instagram
    def two_step(self, code):
        password_vry = self.driver.find_element_by_xpath("//input[@name='verificationCode']")
        password_vry.clear()
        password_vry.send_keys(code)
        password_vry.send_keys(Keys.RETURN)
        time.sleep(self.sleep)
        while True:
            try:
                self.driver.find_element_by_xpath("//p[@id='twoFactorErrorAlert']")
                self.letter["response"] = mutual.incorrectPass
                return self.letter
            except NoSuchElementException:
                print("such kind of elements didn't find")
                break
        self.letter["response"]= mutual.successLogin
        return self.letter


# A function to save cookies
def save_cookies(username, cookies):

        file = open("../../inf/cookies/" + username + ".data", "w+")
        for cookie in cookies:
            file.write(str(cookie) + '\n')


# A function to get unique id information fast to sign up
def get_fast_id(username):
    info = get_req_url(username)
    id_index = re.search('\"id\":', info)
    return info[id_index.end()+1:id_index.end() + 11]


# getting post numbers and other personal data
def get_public_informations(username):

    informations = {
        "postNum": -1,
        "folwerNum": -1,
        "folwngNum": -1,
        "bio": "",
        "img_url": ""
    }

    info = get_req_url(username)

    # getting the bio of the user
    informations["bio"] = find_bio(info)

    # getting post numbers information
    infArr = find_routine_info(info)

    informations["folwerNum"] = infArr[0]
    informations["folwngNum"] = infArr[1]
    informations["postNum"] = infArr[2]
    informations["img_url"] = find_img_url(info)


# finding image url for
def find_img_url(info):
    start_index = re.search("\"profile_pic_url_hd\":", info).end()
    last_index = re.search("\"requested_by_viewer\"", info).start()
    print(info[start_index+1: last_index - 2])
    return info[start_index: last_index - 1]


# finding the bio of a username in html request
def find_bio(info):
    bio_start_index = re.search("\"biography\":", info).end()
    bio_end_index = re.search("\"blocked_by_viewer\":", info).start()
    return info[bio_start_index + 1: bio_end_index - 2]


# finding the number of follower , ...
def find_routine_info(info):
    meta_start_index = re.search("<meta content", info).end()

    end_alphabet = ""
    meta_stop_index = meta_start_index
    while end_alphabet != "-":
        meta_stop_index += 1
        end_alphabet = info[meta_stop_index]
    informations = info[meta_start_index + 2: meta_stop_index]

    finalInfo = informations.split(",")

    for i in range(len(finalInfo) - 1):
        finalInfo[i] = finalInfo[i].replace(" ", "")
        temp = finalInfo[i]
        finalInfo[i] = temp[0:temp.index("F")]

    temp = finalInfo[2]
    finalInfo[2] = temp[0:temp.index('P')]

    for i in range(len(finalInfo)):
        finalInfo[i] = int(finalInfo[i])
    return finalInfo


# getting the html page
def get_req_url(username):
    url = "https://www.instagram.com/" + username + "/"
    return requests.get(url).text


