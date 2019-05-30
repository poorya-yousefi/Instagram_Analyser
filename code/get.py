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
  # get page name and creat a list of followers
    def get_followers_list(self, pagename):

        file = open("/root/Desktop/py/database/"+pagename+"followers.txt","w+")
        sleep = 4
        driver = self.driver

        try:
            driver.get("https://www.instagram.com/" + pagename + "/")
            time.sleep(sleep)
            allfoll = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"))
            allfoll = allfoll.get_attribute('title')
            allfoll = allfoll.replace(',', '')
            allfoll = int(allfoll)
            followers_button = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a")
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
            SCROLL_PAUSE_TIME = 2
            # Get scroll height
            last_height = driver.execute_script("return arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            # userslist = []
            cc = 0
            userslistget = driver.find_elements_by_xpath("//div[@class='d7ByH']/a")

            while cc<=4:
                if len(userslistget) <= allfoll - 3:
                    while True:
                        # Scroll down to bottom
                        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                        # Wait to load page
                        time.sleep(SCROLL_PAUSE_TIME)
                        # Calculate new scroll height and compare with last scroll height
                        new_height = driver.execute_script("return arguments[0].scrollTop = arguments[0].scrollHeight",dialog)
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
            file.write("page name is:\n{}\n".format(pagename))
            if len(userslistget) <= allfoll - 5:
                print("broken file")
                file.write("broken file"+"\n")
            for user in userslistget:
                print(user.get_attribute("title"))
                file.write(str(user.get_attribute("title"))+"\n")
            file.write(str(len(userslistget)))
            print(len(userslistget))
            file.close()
        except NoSuchElementException:
            pass


    def find_network(self,filename):
        file=open("/root/Desktop/py/clean/"+filename+".txt")
        done_file = open("/root/Desktop/py/done/" + filename + ".txt", "a+")
        breakpointfile = open("/root/Desktop/py/done/" + filename + "breakpoint.txt","a+")
        breakpointfile.write("0"+"\n")
        breakpointfile.close()
        breakpointfile = open("/root/Desktop/py/done/" + filename + "breakpoint.txt","r+")
        read_breakpointfile = breakpointfile.readlines()
        # print(str(read_file))
        # print(str(read_breakpointfile))
        try:
            breakpointcount = read_breakpointfile[-2]
        except:
            breakpointcount = read_breakpointfile[-1]
        read_file=file.readlines()
        print(breakpointcount)
        print(int(read_file[-1]))
        for i in range(int(breakpointcount),int(read_file[-1])):
            a= read_file[i].replace("[","")
            b = a.replace("]","")
            c= b.replace(",","")
            try:
                self.driver.get("https://www.instagram.com/" + c + "/")
                # print(self.driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title"))
                q = self.driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
                q = q.replace(",", "")
                breakpointcount = int(breakpointcount) + 1
                breakpointfile.write(str(breakpointcount) + "\n")
                # print(q)
                if int(q) <= int(2000):
                    done_file.write(c + "\n")
                    print(c)
                    print(q)
                    hemin.get_followers_list(c)
            except NoSuchElementException:
                breakpointcount = int(breakpointcount) + 1
                breakpointfile.write(str(breakpointcount) + "\n")
                pass
        done_file.close()
        file.close()

    def get_liker(self, pagename):
        def get_liker(self, pagename):
            file = open("/home/hem/Desktop/py/instagram/liker/" + pagename + "liker.txt", "a+")
            sleep = 3
            driver = self.driver
            driver.get("https://www.instagram.com/" + pagename + "/")
            time.sleep(2)
            u = driver.find_element_by_class_name('g47SY')
            print(u.text)

            pic_hrefs = []
            for i in range(1, int(int(u.text) / 8)):
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    # get tags
                    hrefs_in_view = driver.find_elements_by_tag_name('a')
                    # finding releveant hrefs
                    # print(elem.get_attribute('href'))
                    url = "https://www.instagram.com/p/"

                    hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if
                                     url in elem.get_attribute('href')]
                    # print(hrefs_in_view)
                    # building list of unique photos
                    [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                    # print("check: pic href length" + str(len(pic_hrefs)))
                except Exception as e:
                    print('exception hapen ', e)
                    continue
            try:
                count = 0
                for w in range(len(pic_hrefs)):
                    post_number = w + 1
                    try:

                        go_to_pic = driver.get(pic_hrefs[w])
                        like_button = driver.find_element_by_class_name("zV_Nj")
                        like_button.click()
                        a = like_button.text
                        c = re.findall(r"(.*\d)", str(a))
                        n = c[0].replace(',', '')
                        allfoll = (int(n))
                        time.sleep(sleep)
                        driver.implicitly_wait(2)
                        dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div')
                        driver.set_script_timeout(2)
                        driver.implicitly_wait(4)
                        time.sleep(sleep)
                        s = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div")
                        # scroll down the page
                        s.location_once_scrolled_into_view
                        time.sleep(3)
                        file.write(str(post_number) + "\n")
                        userslist = driver.find_elements_by_xpath(
                            "//div[@class='_7UhW9   xLCgt      MMzan  KV-D4            fDxYl     ']/a")
                        for user in userslist:
                            # a.append(user.get_attribute("title"))
                            # print(user.get_attribute("title"))
                            file.write(str(user.get_attribute("title")) + "\n")

                        for i in range(int(allfoll / 12)):
                            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                            time.sleep(1)
                            # print("Extracting friends %", round((i / (allfoll / 2) * 100), 2), "from", "%100")
                            userslist = driver.find_elements_by_xpath(
                                "//div[@class='_7UhW9   xLCgt      MMzan  KV-D4            fDxYl     ']/a")
                            for user in userslist:
                                # a.append(user.get_attribute("title"))
                                # print(user.get_attribute("title"))
                                file.write(str(user.get_attribute("title")))
                                file.write("\n")

                        url = "https://www.instagram.com/"
                        # print(users)
                        # users = [href for href in users if url in href]
                        #     print(users, "\n", len(users))
                        file.write(str(user.get_attribute("title")))
                        file.write("\n")
                        # file.write(str(len(user)))
                        # print("ok1",count)
                        count = count + 1
                    except:

                        go_to_pic = driver.get(pic_hrefs[w])
                        u = driver.find_element_by_xpath(
                            "/html/body/span/section/main/div/div/article/div[2]/section[2]/div/div[2]/a[2]")
                        u.click()
                        time.sleep(2)
                        a = u.text

                        c = re.findall(r"(.*\d)", str(a))

                        n = c[0].replace(',', '')

                        allfoll = (int(n))
                        time.sleep(sleep)
                        driver.implicitly_wait(2)
                        dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div')
                        driver.implicitly_wait(4)
                        time.sleep(sleep)
                        s = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div")

                        # scroll down the page

                        s.location_once_scrolled_into_view
                        time.sleep(3)
                        # print("ok2")
                        # b = []
                        file.write(str(post_number))
                        file.write("\n")
                        userslist = driver.find_elements_by_xpath(
                            "//div[@class='_7UhW9   xLCgt      MMzan  KV-D4            fDxYl     ']/a")
                        for user in userslist:
                            # a.append(user.get_attribute("title"))
                            # print(user.get_attribute("title"))
                            file.write(str(user.get_attribute("title")))
                            file.write("\n")
                        for i in range(int(allfoll / 12)):
                            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                            time.sleep(1)
                            print("Extracting friends %", round((i / (allfoll / 2) * 100), 2), "from", "%100")
                            userslist = driver.find_elements_by_xpath(
                                "//div[@class='_7UhW9   xLCgt      MMzan  KV-D4            fDxYl     ']/a")
                            for user in userslist:
                                # b.append(user.get_attribute("title"))
                                # print(user.get_attribute("title"))
                                file.write(str(user.get_attribute("title")))
                                file.write("\n")

                        url = "https://www.instagram.com/"
                        # print(users)
                        # users = [href for href in users if url in href]
                        #     print(users, "\n", len(users))
                        # file2.write(str(b))
                        # file.write(str(user.get_attribute("title")))

                        # file.write(str(len(users)))
                        # print("ok2",count)
                        count = count + 1
            except NoSuchElementException as e:
                print(e)
            file.close()
            # return user_comment


hemin = InstagramBot()
hemin.login()
hemin.get_followers_list("guilan.fanni")
# hemin.find_network("guilan.humanitiesclean")
# hemin.get_liker("hemin.saed")