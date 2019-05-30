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


@app.route("/sign_up", methods=["POST"])
def sign_up_handler():
    if not request.is_json:
        letter = {
            "response": mutual.unknownError
        }
        return jsonify(letter)
    else:
        # getting the json file from client
        content = request.get_json()

        # trying to login to the page to see can we login or not
        user = Login.Login(content["username"], content["password"])

        # check that can we log as a username or not
        result = user.login()

        uniqueID = Login.get_fast_id(content["username"])

        if instaUsers_db.get_user(db, uniqueID, instaUsers_db.col_unique_id) is not None:
            if appUsers_db.get_user(db, uniqueID, select_arg="unique_id") is not None:
                result["response"] = mutual.existingUser
                return result["response"]
            # if we have an instaUser just make an app user
            else:
                # userInformation = Login.get_public_informations(content["username"])
                newAppUser = appUser.CommercialUser(uniqueID, datetime.datetime.now(), False, content["country"],
                                                    content["city"],
                                                    content["phone_num"], content["personality_key_words"], "", "",
                                                    content["company_name"], content["activity"])
                appUsers_db.insert_user(db, newAppUser)
                editedInstaUser = instaUsers_db.get_user(db, uniqueID, select_arg=uniqueID)
                editedInstaUser.appUserId = appUsers_db.get_user()

                return result

        if result["response"] == "000":
            print("A success login for " + content["username"])

            if content["topic"] == mutual.commercialUser:
                userInformation = Login.get_public_informations(content["username"])
                newInstaUser = instaUser.InstaUser(-1, content["username"], uniqueID, userInformation["is_private"],
                                                   userInformation["postNum"], userInformation["folwerNum"],
                                                   userInformation["folwngNum"], content["page_type"],
                                                   userInformation["img_url"], userInformation["bio"])

                instaUsers_db.insert_user(db, newInstaUser)

                newAppUser = appUser.CommercialUser(datetime.datetime.now(), False, content["country"], content["city"],
                                                    content["phone_num"], content["personality_key_words"], "", "",
                                                    content["company_name"], content["activity"])
                appUsers_db.insert_user(db, newAppUser)

                # newInstaUser.appUserId = appUsers_db.get_user(db, newAppUser.userId).userId

        return result


@app.route("/first_page_info", methods=["GET", "POST"])
def first_page_info():
    # find the cookie and start the following commands
    if not request.is_json:
        letter = {
            "response": mutual.unknownError
        }
        return jsonify(letter)
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
        letter = {
            "response": mutual.unknownError
        }
        return jsonify(letter)


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
        letter = {
            "response": mutual.unknownError
        }
        return jsonify(letter)


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
        letter = {
            "response": mutual.unknownError
        }
        return jsonify(letter)


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
        letter = {
            "response": mutual.unknownError
        }
        return jsonify(letter)


if __name__ == "__main__":
    db = mysql.connector.connect(**serverConfig.server_config)
    print("db connected successfully")
    app.run()
