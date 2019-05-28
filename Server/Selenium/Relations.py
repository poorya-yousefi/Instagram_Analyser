import ast
from selenium import webdriver

# common errors
no_cookie = "No cookie was found for this username "


def get_relations(username):

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
        return "can not log in with cookie, please retry"
    else:
        print("logged in successfully")
        return "logged in successfully"


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
get_relations("iBotErfan")