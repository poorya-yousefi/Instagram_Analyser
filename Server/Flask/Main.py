from flask import Flask
from flask import request
from flask import jsonify
from Server.Selenium import Login, Relations
from DataBase import appUser, appUsers_db
from DataBase import instaUser, instaUsers_db
from DataBase import serverConfig
from Mutual import mutual
import datetime
import mysql.connector


# defining data base
db = None

app = Flask(__name__)


dic = {
    "user": None
}


# Common Errors
notJson = "Login Failed, The received file is not json."


@app.route("/sign_up", methods=["POST"])
def sign_up():
    if not request.is_json:
        return jsonify({'error': 'not json'})
    else:
        # getting the json file from client
        content = request.get_json()

        # trying to login to the page to see can we login or not
        user = Login.Login(content["username"], content["password"])

        # check that can we log as a username or not
        result = user.login()
        if result["response"] == "000":
            print("A success login for " + content["username"])

            # check for that which this user exists or not

            if content["topic"] == mutual.commercialUser:
                userInformation = Login.get_public_informations(content["username"])
                newAppUser = appUser.CommercialUser(datetime.datetime.now(), False, content["country"], content["city"],
                                                    content["phone_num"], content["personality_key_words"], "", "",
                                                    content["company_name"], content["activity"])
                appUsers_db.insert_user()
                newInstaUser = instaUser.InstaUser(newAppUser.userId)
        return result


@app.route("/first_page_info", methods=["GET", "POST"])
def first_page_info():
    # configure to know who is online
    # find the cookie and start the following commands
    if not request.is_json:
        return jsonify({'error': 'not json'})
    # Getting post numbers
    # compare new post numbers with database

    # Getting followers numbers
    # compare new followers numbers with database

    # Getting followings numbers
    # compare new followings numbers with database

    # return new parameters number and difference new and old
    return jsonify(
        {
            'posts': 17,
            'followers': 250,
            'followings': 278
        }
    )


# listening on port = "127.0.0.1" on port 50000 for login
@app.route('/login', methods=['POST', 'GET'])
def login_handler():
    if request.is_json:
        print("Login Json received successfully ... ")
        content = request.get_json()
        print("Login Json contents: ", content)

        # Check the database for username and password
        app = appUser.AppUser(datetime.datetime.now(), )

        # log in to the page with selenium
        user = Login.Login(content["username"], content["password"])
        result = user.login()
        dic["user"] = user

        if result["result"] == "two step is enable":
            return result["result"]
        else:
            return result["result"]

    else:
        return notJson


# listening on port = "127.0.0.1" on port 50000 for two Step verification code
@app.route("/twoStep", methods=['POST', 'GET'])
def two_step_handler():
    if request.is_json:
        print("two step verification received ... ")
        content = request.get_json()
        print("two step verification json contents is : ", content)
        # getting the Login objects
        user = dic["user"]
        result = user.two_step(content['code'])
        print(result['result'])
        return result['result']
    else:
        print(notJson)
        return notJson


@app.route("/getFollowers", methods=['POST'])
def get_followers_list_handler():
    if request.is_json:
        print("Get followers json is received")
        content = request.get_json()
        print("Get followers json contents is : ", content)

        # getting the Login objects
        # user = dic["user"]

        # saving objects to
        # followers = user.get_followers_list(content['username'], "followers")
        # return followers
        followings = Relations.get_relations(content["username"], "followers")

        return jsonify(followings)

    else:
        print(notJson)
        return notJson


@app.route("/getFollowing", methods=['POST', 'GET'])
def get_following_list_handler():
    if request.is_json:
        print("Get following json is received")
        content = request.get_json()
        print("Get following json contents is : ", content)

        following = Relations.get_relations(content['username'], "followings")
        print("Following done")
        return "done"

    else:
        print(notJson)
        return notJson


if __name__ == "__main__":
    db = mysql.connector.connect(**serverConfig.server_config)
    print("db connected successfully")
    app.run()
