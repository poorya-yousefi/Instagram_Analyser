from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from timeit import default_timer as timer

import re
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import requests
import random

start = timer()
class InstagramBot:

    def __init__(self):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image',2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
        self.driver = webdriver.Firefox(executable_path=r"/root/Desktop/py/geckodriver", firefox_profile=firefox_profile)
        # self.driver.manage().getCookies()

    def closeBrowser(self):
        self.driver.close()

    def login(self):

        sleep = 4
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        # time.sleep(sleep)
        # login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        # login_button.click()
        time.sleep(sleep)
        username = input("username:  ")
        password=input("password:  ")
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(username)
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(sleep)
        while True:
            try:
                driver.find_element_by_xpath("//p[@id='slfErrorAlert']")
                print("The username or password is wrong")
                username = input("username:  ")
                password = input("password:  ")
                user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
                user_name_elem.clear()
                user_name_elem.send_keys(username)
                password_elem = driver.find_element_by_xpath("//input[@name='password']")
                password_elem.clear()
                password_elem.send_keys(password)
                password_elem.send_keys(Keys.RETURN)
                time.sleep(sleep)
            except NoSuchElementException:
                break


        while True:
            try:
                driver.find_element_by_xpath("//input[@name='verificationCode']")
                vrypassword = input("two factor authentication:  ")
                passsword_vry = driver.find_element_by_xpath("//input[@name='verificationCode']")
                passsword_vry.clear()
                passsword_vry.send_keys(vrypassword)
                passsword_vry.send_keys(Keys.RETURN)
                time.sleep(sleep)
            except NoSuchElementException:
                break
        print("login succesful")

    def get_liker(self, pagename):
        file = open("/root/Desktop/py/database/likerid/" + pagename + "liker.txt", "a+")
        sleep = 3
        driver = self.driver
        driver.get("https://www.instagram.com/" + pagename + "/")
        time.sleep(2)
        u = driver.find_element_by_class_name('g47SY')
        print(u.text)
        pic_hrefs = []

        SCROLL_PAUSE_TIME = 1
        nim = 0
        cc = 0
        user_list = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        userslistget = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a")
        for user in userslistget:
            print(user.get_attribute("href"))
            user_list.append(user)
        print("userpic len", len(user_list))
        while cc <= 4:
            if len(user_list) <= int(u.text) - 3:
                while True:
                    # Scroll down to bottom
                    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # Wait to load page
                    time.sleep(SCROLL_PAUSE_TIME)
                    # Calculate new scroll height and compare with last scroll height
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                    nim = nim + 1
                    print(nim)
                    userslistget = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a")
                    for user in userslistget:
                        print(user.get_attribute("href"))
                        user_list.append(user)

                print("userpic len", len(user_list))
                cc = cc + 1
            else:
                break



hemin = InstagramBot()
hemin.login()
hemin.get_liker("diesel")
# iBotErfan


