from selenium import webdriver
import time
import ast

# common errors
no_cookie = "No cookie was found for this username "
sleep = 25

def get_relations(username, connection_type):
    content, driver = login_with_cookies(username)
    if content == "success":
         get_followers_list(username, connection_type, driver)
    else :
        return content


def login_with_cookies(username):
    cookies = get_cookie(username)

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    driver = webdriver.Firefox(executable_path=r"C:\Users\erfan\.wdm\geckodriver\v0.24.0\win64\geckodriver.exe",
                               firefox_profile=firefox_profile)
    driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
    current_url = driver.current_url
    if current_url == 'https://www.instagram.com/accounts/login/?source=auth_switcher':
        print("can not log in with cookie, please retry")
        return "can not log in with cookie, please retry" , driver
    else:
        return "success", driver


def get_cookie(username):
    try:
        file = open("../../inf/cookies/" + username + ".data", "r")
        # find cookies using database
    except FileNotFoundError:
        print(no_cookie)
        return no_cookie

    cookie = []

    for line in file:
        cookie.append(ast.literal_eval(line))

    return cookie


def get_followers_list(pagename, connection_type, driver):
        followers = ""
        sleep = 5
        users = []


        try:
            driver.get("https://www.instagram.com/" + pagename + "/")
            time.sleep(sleep)
            allfoll = (
                driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"))
            allfoll = allfoll.get_attribute('title')
            allfoll = allfoll.replace(',', '')
            allfoll = int(allfoll)

            if connection_type == "followers":
                followers_button = driver.find_element_by_xpath(
                    "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a")
            elif connection_type == "followings":
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
                users.append(str(user.get_attribute("title")))


        except Exception:
            print("exception happened ")
            pass
        driver.close()
        return users


# following one person on instagram with id
def request(username, target_username, driver):

    driver.get("https://www.instagram.com/" + target_username + "/")
    time.sleep(10)
    button = driver.find_element_by_xpath(
            "/html/body/span/section/main/div/header/section/div[1]/button")

    if button.text == 'Following':
        print("User with id " + username + " wants to follow " + target_username + " but was following before. !!!\n")
        return "User with id " + username + " wants to follow " + target_username + " but was following before. !!!"
    elif button.text == "Requested":
        print("User with id " + username + " wants to follow " + target_username + " but was requested before. !!!\n")
        return "User with id " + username + " wants to follow " + target_username + " but was requested before. !!!"
    else:
        time.sleep(5)
        following_button = driver.find_element_by_xpath(
         "/html/body/span/section/main/div/header/section/div[1]/button")
        following_button.click()
        time.sleep(sleep)
        print("User with id " + username + " send a follow request to " + target_username + "!!\n")
        return "Following or requesting "


def request_list(username, following_list, driver):
    sleep = 25
    for i in range(len(following_list)):
        request(username, following_list[i], driver)
        sleep
    return "Requested Successfully"


def add_relation(username, following_list):
    content, driver = login_with_cookies(username)
    if content == "success":
       return request_list(username, following_list, driver)
    else:
        return content


