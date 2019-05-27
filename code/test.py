
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

    def __init__(self, username, password):

        self.username = username
        self.password = password
        # chrome_options = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images":2}
        # chrome_options.add_experimental_option("prefs",prefs)
        # self.driver = webdriver.Chrome(executable_path=r"/root/Desktop/py/chromedriver", chrome_options=chrome_options)
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image',2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
        self.driver = webdriver.Firefox(executable_path=r"/root/Desktop/py/geckodriver", firefox_profile=firefox_profile)


    def closeBrowser(self):
        self.driver.close()

    def login(self):

        sleep = 3
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(sleep)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(sleep)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(sleep)
        time.sleep(20)

    def driver_go(self,c):
        driver = self.driver
        driver.get("https://www.instagram.com/"+c+"/")
        time.sleep(2)
        allfoll = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"))
        allfoll = allfoll.get_attribute('title')
        allfoll = allfoll.replace(',', '')
        allfoll = int(allfoll)
        return allfoll
  # get page name and creat a list of followers
    def get_followers_list(self, pagename):

        file = open("/root/Desktop/py/followerslist/"+pagename+"followers.txt","a+")
        sleep = 2
        driver = self.driver
        driver.get("https://www.instagram.com/"+pagename+"/")
        time.sleep(sleep)
        allfoll = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"))
        allfoll = allfoll.get_attribute('title')
        allfoll = allfoll.replace(',', '')
        allfoll = int(allfoll)
        # if int(allfoll)>=int(3000):

        followers_button = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a")
        followers_button.click()
        time.sleep(sleep)
        driver.implicitly_wait(2)
        dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]')

        driver.implicitly_wait(2)
        time.sleep(sleep)
        s = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div")

        # scroll down the page

        s.location_once_scrolled_into_view
        time.sleep(sleep)
        nim = 0
        # a=[]
        # userslist = driver.find_elements_by_xpath("/html/body/div[3]/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/a")
        # for user in userslist:
        #     a.append(user.get_attribute("title"))
        #     print(user.get_attribute("title"))
        #     file.write(str(user.get_attribute("title")))
        #     file.write("\n")
        for i in range(int(allfoll / 11)):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            time.sleep(1)
            nim = nim+1
            print(nim,"  ","Extracting friends %", round((i / (allfoll / 2) * 100), 2), "from", "%100")


            ###get another way
        # userslist = driver.find_elements_by_xpath("div[@class='']/a")
        # for user in userslist:
        #         a.append(user.get_attribute("title"))
        #     print(len(user.get_attribute("title")))
            # file.write(str(user.get_attribute("title")))
            # file.write("\n")
            # "class=W1Bne   ztp9m "



        ### get all users one time

        taga    =   driver.find_elements_by_tag_name('a')
        users = [elem.get_attribute('href') for elem in taga if elem.get_attribute('class') == "FPmhX notranslate _0imsa "]
        url = "https://www.instagram.com/"
        users = [href for href in users if url in href]

        print(users , "\n", len(users))
        file.write(str(users))
        file.write("\n")
        file.write(str(len(users)))
        file.close()

    def get_following_list(self, pagename):

            file = open("/root/Desktop/py/following list/" + pagename + "following.txt", "a+")
            sleep = 1
            driver = self.driver
            driver.get("https://www.instagram.com/" + pagename + "/")
            time.sleep(sleep)
            allfoll = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span"))
            print(allfoll.text)
            allfoll = allfoll.text
            # allfoll = allfoll.get_attribute('text')
            # print(allfoll)
            allfoll = allfoll.replace(',', '')
            allfoll = int(allfoll)
            followers_button = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a")
            followers_button.click()
            time.sleep(sleep)
            pepole_button = driver.find_element_by_xpath("/html/body/div[3]/div/nav/a[1]")
            pepole_button.click()
            dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]')
            s = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div")

            # scroll down the page

            s.location_once_scrolled_into_view
            # s.location_once_scrolled_into_view
            # s.location_once_scrolled_into_view
            time.sleep(sleep)
            for i in range(int(allfoll /12)):
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                time.sleep(0.8)
                print("Extracting friends %", round((i / (allfoll / 2) * 100), 2), "from", "%100")

            taga = driver.find_elements_by_tag_name('a')
            users = [elem.get_attribute('href') for elem in taga if
                     elem.get_attribute('class') == "FPmhX notranslate _0imsa "]
            url = "https://www.instagram.com/"
            users = [href for href in users if url in href]

            print(users, "\n", len(users))
            file.write(str(users))
            file.write("\n")
            file.write(str(len(users)))
            file.close()

            # get missy list and give back a clean list is just name

        # get missy list and give back a clean list is just name
    def clean_list(self,pagename):
        a = input("1-follower/2-following:  ")
        def openfile(pagename):
            if a =="1":
                open_file = open("/root/Desktop/py/followerslist/"+pagename+"followers.txt", "r+")
                read = open_file.read()
                return read
                open_file.close()
            if a =="2":
                open_file = open("/root/Desktop/py/following list/" + pagename + "following.txt", "r+")
                read = open_file.read()
                return read
                open_file.close()
        read = openfile(pagename)
        re = read.replace("'https://www.instagram.com/", "")
        me = re.replace("/'", "")
        de = me.replace(" ", "\n")
        if a == "1":
            he = open("/root/Desktop/py/clean/"+pagename + "followersclean.txt", "w+")
            he.write(de)
            he.close()
        elif a == "2":
            he = open("/root/Desktop/py/clean/"+pagename + "followingclean.txt", "w+")
            he.write(de)
            he.close()
   #  get list and following pepole at the list
    def followering_pepole(self, listofname):

        sleep = 25
        driver = self.driver
        list_name=open(listofname+".txt","r+")
        k = list_name.readlines()
        a = re.findall(r"'(.*?),", str(k))
        lista = a
        count = 0
        print(lista)
        print(len(lista))
        for i in range(1, int(len(lista)/2)):
            start = timer()
            x=(i*2)
            user = lista[x]
            driver.get("https://www.instagram.com/"+user+"/")
            print(count)
            try:
                print(driver.find_element_by_xpath(".//span[@class = 'vBF20 _1OSdk']").text)
                if driver.find_element_by_xpath(".//span[@class = 'vBF20 _1OSdk']").text != 'Following':
                    try:
                        following_button = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/span/span[1]/button")
                        following_button.click()
                        time.sleep(sleep)
                        end = timer()
                        count = count + 1
                        print("Time taken:", end - start)
                    except NoSuchElementException:
                        try:
                            following_button = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/button")
                            following_button.click()
                            time.sleep(sleep)
                            end = timer()
                            count = count + 1
                            print("Time taken:", end - start)
                        except NoSuchElementException:
                            time.sleep(sleep)
                            end = timer()
                            print("Time taken:", end - start)
                            pass
            except NoSuchElementException:
                pass

    def like_photo(self,hashtag):

        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/"+hashtag+"/")
        time.sleep(2)
        for i in range(1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # searching for pichuer link
        hrefs = driver.find_elements_by_tag_name('a')
        print(len(hrefs))
        pic_hrefs=[elem.get_attribute('href') for elem in hrefs]
        print(pic_hrefs)

        url="https://www.instagram.com/p/"
        pic_hrefs = [href for href in pic_hrefs if url in href]

        print(pic_hrefs)
        print(hashtag+ 'photos: '+str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:

                button=driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[2]/section[1]/span[1]/button")

                print(button.text)
                if driver.find_element_by_xpath(".//span[@class = 'glyphsSpriteHeart__outline__24__grey_9 u-__7']").get_attribute("aria-label") == "Like":

                    button.click()
                    time.sleep(18)
            except Exception as e:
                print(e)
                time.sleep(2)
    # count your follwers have how much follwers and give you a wight
    def count_follwers_offollowers(self,file_address):

        # t = input("file name: ")
        file = open(file_address + ".txt", "r+")
        save = open(file_address + "analysis.txt", "a+")
        k = file.readlines()
        print("1", str(k))
        a = re.findall(r"'(.*?),", str(k))
        print("2", a)
        lista = a
        print("3", len(lista))
        count = 0
        for i in range(1, int((len(lista) / 2))):
            x = i * 2
            user = lista[x]
            print(count, user)
            count = count + 1
            url = 'https://www.instagram.com/' + user
            r = requests.get(url).text
            start = '"edge_followed_by":{"count":'
            end = '},"followed_by_viewer"'
            print("followers number: ", r[r.find(start) + len(start):r.rfind(end)])
            save.write(str(count) + " : " + user + "\n" + "followers number: " + str(
                r[r.find(start) + len(start):r.rfind(end)]) + "\n")
        file.close()
        save.close()

    def avrage(self,file_address):

        # t = input("file name: ")
        file = open(file_address + ".txt", "r+")
        save = open(file_address + "ava.txt", "a+")
        k = file.readlines()
        print("1", str(k))
        a = re.findall(r"'(.*?),", str(k))
        print("2", a)
        lista = a
        print("3", len(lista))
        count = 0
        m = []
        n = 0
        for i in range(1, int((len(lista) / 2))):
            x = i * 2
            user = lista[x]
            print(count, user)
            count = count + 1
            url = 'https://www.instagram.com/' + user
            r = requests.get(url).text
            start = '"edge_followed_by":{"count":'
            end = '},"followed_by_viewer"'
            mx = (r[r.find(start) + len(start):r.rfind(end)])

            print(mx)
            m.append(mx)
            save.write(str(mx) + "\n")
            n=n+int(mx)
            print("ava: ",n/count)
        f = 0
        for n in (len(m)-1):
            f = (f + int(m[n])) / (len(m) + 1)
            print(f)
        file.close()
        save.close()

    def get_pictures_on_page(self, hashtag, scrolls=int):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/"+hashtag+"/")
        time.sleep(2)
        #gathering photos
        pic_hrefs = []
        for i in range(1, scrolls):
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
                print(hrefs_in_view)
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("check: pic href length" + str(len(pic_hrefs)))
            except Exception as e:
                print('exception hapen ',e)
                continue
        print(pic_hrefs)
        return pic_hrefs
    # write comment in text area using lambda function
    def write_comment(self, comment_text):
        driver = self.driver
        try:
            # comment_button = lambda: self.driver.find_element_by_xpath(".//button[@class = 'dCJp8 afkep _0mzm-']")
            comment_button = lambda: self.driver.find_element_by_xpath(".//span[@class = 'glyphsSpriteComment__outline__24__grey_9 u-__7']")
            if self.driver.find_element_by_xpath(".//span[@class = 'glyphsSpriteComment__outline__24__grey_9 u-__7']").get_attribute("aria-label") == "Comment":
            # comment_button = lambda: self.driver.find_element_by_link_text('Comment')
                comment_button.click()
                time.sleep(2)
        except NoSuchElementException and Exception:
            pass

        try:
            driver.find_element_by_xpath("//textarea[@class = 'Ypffh']").click()
            driver.find_element_by_xpath("//textarea[@class = 'Ypffh']").clear()
            driver.find_element_by_xpath("//textarea[@class = 'Ypffh']").send_keys('')
            comment_box_elem = lambda: driver.find_element_by_xpath("//textarea[@class = 'Ypffh']")

            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep(0.1)

            return comment_box_elem

        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False

    #actually post a comment
    def post_comment(self, comment_text):
        time.sleep(random.randint(1,5))

        comment_box_elem = self.write_comment(comment_text)
        if comment_text in self.driver.page_source:
            comment_box_elem().send_keys(Keys.ENTER)
            try:
                post_button = lambda: self.driver.find_element_by_xpath("//button[@type='Post']")
                post_button().click()
                print("click post button")
            except NoSuchElementException:
                pass
        time.sleep(random.randint(4, 6))
        self.driver.refresh()
        if comment_text in self.driver.page_source:
            return True
        return False

    def get_comments(self,pagename):
        file = open("/home/hem/Desktop/py/instagram/comment/"+pagename+"comment.txt","a+")
        #load comment if button exists
        driver = self.driver
        driver.get("https://www.instagram.com/"+pagename+"/")
        time.sleep(2)
        u = driver.find_element_by_class_name('g47SY')
        print(u.text)

        pic_hrefs = []
        for i in range(1, int(int(u.text)/8)):
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
                print('exception hapen ',e)
                continue
        # print(pic_hrefs)
        try:
            number = 0
            for w in range(len(pic_hrefs)):

                go_to_pic = driver.get(pic_hrefs[w])
                elem_coment_block = driver.find_elements_by_class_name("gElp9 ")
                print(elem_coment_block)
                print(len(elem_coment_block))
                count = 0
                number = number + 1
                for i in range(0, len(elem_coment_block)):
                    user_comment = elem_coment_block[i].find_element_by_tag_name("span")
                    print(number,"  ",count,"  ", user_comment)
                    file.write(str(number)+"  "+str(count)+"  "+elem_coment_block[i].text+"\n")
                    count = count + 1

        except NoSuchElementException as e:
            print(e)
        file.close()
        # return user_comment
    def get_liker(self, pagename):
        file = open("/home/hem/Desktop/py/instagram/liker/" + pagename + "liker.tx", "a+")
        sleep = 3
        driver = self.driver
        driver.get("https://www.instagram.com/"+pagename+"/")
        time.sleep(2)
        u = driver.find_element_by_class_name('g47SY')
        print(u.text)

        pic_hrefs = []
        for i in range(1, int(int(u.text)/8)):
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
                print('exception hapen ',e)
                continue
        try:
            count = 0
            for w in range(len(pic_hrefs)):
                post_number = w+1
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
                    # a = []
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
                    count = count+1
                except:


                    go_to_pic = driver.get(pic_hrefs[w])
                    u = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[2]/section[2]/div/div[2]/a[2]")
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
                    count = count+1
        except NoSuchElementException as e:
            print(e)
        file.close()
        # return user_comment

# run part

hemin = InstagramBot("hemin.saed", "mrbot911")
hemin.login()
hemin.get_followers_list("guilan.humanities")
# hemin.clean_list("hedi2165")
# hemin.avrage("/root/Desktop/py/clean/hedi2165followersclean")

# hemin.count_follwers_offollowers("/root/Desktop/py/clean/ab3diinfollowersclean")
# print("""1-get followers list
# 2-get following list
# 3- clean list
# 4- get list and aoutomate""")
# a = input("comend line:  ")
# b= input("run progarm: ")
# while b == "y":
#     if a == "1":
#         hemin.get_followers_list(input("page name:  "))
#     elif a == "2":
#         hemin.get_following_list(input("page name:  "))
#     elif a == "3":
#         hemin.clean_list(input("page name:  "))
#     elif a == "4":
#         page = input("pagename:  ")
#         ff = input("1-followers/2-following:  ")
#         if ff == "1":
#
#             open_file = open("/root/Desktop/py/clean/" + page + "followersclean.txt", "r+")
#             read = open_file.readlines()
#             read = str(read)
#             read = read.replace("[", "")
#             read = read.replace("]", "")
#             read = read.replace(",", "")
#             save = open("/root/Desktop/py/clean/" + page + "followerscleansave.txt", "w+")
#             save.write(read)
#             save.close()
#
#             for w in read:
#                 print(w)
#                 hemin.get_followers_list(w)
#                 hemin.get_following_list(w)
#             open_file.close()
#         elif ff == "2":
#
#             open_file = open("/root/Desktop/py/clean/" + page + "followingclean.txt", "r+")
#             read = open_file.readlines()
#
#             read = str(read)
#             read = read.replace("[", "")
#             read = read.replace("]", "")
#             read = read.replace(",", "")
#             save = open("/root/Desktop/py/clean/" + page + "followingcleansave.txt", "w+")
#             save.write(read)
#             save.close()
#
#             for w in read:
#                 print(w)
#                 hemin.get_followers_list(w)
#                 hemin.get_following_list(w)
#             open_file.close()
#     b = input("run progarm: ")
#     a = input("comend line:  ")

# open_file = open("/root/Desktop/py/clean/hemin.saedfollowersclean.txt", "r+")
# read = open_file.readlines()
# read = read
# for i in range(0,int(read[-1])):
#     a= read[i].replace("[","")
#     b = a.replace("]","")
#     c= b.replace(",","")
#
#     m = hemin.driver_go(c)
#
#     if m <= int(3000):
#         hemin.get_followers_list(c)
#         hemin.get_following_list(c)

    # print(c)
# save = open("/root/Desktop/py/clean/hemin.saedfollowerscleansave.txt", "w+")
# save.write(c)
# save.close()
#
# for w in :
#     print(w)
#     hemin.get_followers_list(w)
#     hemin.get_following_list(w)
# open_file.close()

# hemin.get_followers_list("hemin.saed")
# hemin.get_followers_list("adhamsaadi")
# hemin.clean_list("rhino_handmade")
# andreyIG.get_liker_id("nike")
# hemin.get_comments("soroosh_moradiii")
# hemin.get_liker("")
# hemin.count_follwers_offollowers("/home/hem/Desktop/py/instagram/clean/rhino_handmadeclean")
end = timer()


print("Time taken:", end-start)