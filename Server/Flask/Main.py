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

letter = {
    "response": "",
    "previous_post_num": "",
    "post_num": "",
    "previous_following_num": "",
    "following_num": "",
    "previous_follower_num": "",
    "follower_num": "",
    "img_url": "",
    "name": "",
    "bio": ""
}
dic = {
    "user": None
}


@app.route("/sign_up", methods=["POST", "GET"])
def sign_up_handler():
    if not request.is_json:
        letter["response"] = mutual.unknown_error
        return jsonify(letter)
    else:
        # getting the json file from client
        content = request.get_json()

        # trying to login to the page to see can we login or not
        user = Login.Login(content["username"], content["password"])

        # check that can we log as a username or not
        result = user.login()

        unique_id = Login.get_fast_id(content["username"])

        if instaUsers_db.get_user(db, unique_id, instaUsers_db.col_unique_id) is not None:
            if appUsers_db.get_user(db, unique_id) is not None:
                result["response"] = mutual.existing_user
                return jsonify(result)
            # if we have an instaUser just make an app user
            else:
                # user_information = Login.get_public_informations(content["username"])
                new_app_user = appUser.CommercialUser(unique_id, datetime.datetime.now(), False, content["country"],
                                                      content["city"],
                                                      content["phone_num"], content["personality_key_words"], "", "",
                                                      content["company_name"], content["activity"])
                appUsers_db.insert_user(db, new_app_user)
                return jsonify(result)

        if result["response"] == mutual.success_login:
            print("A success sign up for " + content["username"] + ". ")

            if content["topic"] == mutual.commercial_user:
                user_information = Login.get_public_informations(content["username"])
                new_insta_user = instaUser.InstaUser(unique_id, content["username"], unique_id,
                                                     user_information["is_private"],
                                                     user_information["post_num"], user_information["follower_num"],
                                                     user_information["following_num"], content["page_type"],
                                                     user_information["img_url"], user_information["bio"],
                                                     user_information["name"])

                instaUsers_db.insert_user(db, new_insta_user)

                new_app_user = appUser.CommercialUser(unique_id, datetime.datetime.now(), False, content["country"],
                                                      content["city"],
                                                      content["phone_num"], content["personality_key_words"], "", "",
                                                      content["company_name"], content["activity"])
                appUsers_db.insert_user(db, new_app_user)

                # new_insta_user.appUserId = appUsers_db.get_user(db, new_app_user.userId).userId

        return jsonify(result)


@app.route("/first_page_info", methods=["GET", "POST"])
def first_page_info():
    # find the cookie and start the following commands
    if not request.is_json:
        letter["response"] = mutual.unknown_error
        return jsonify(letter)

    # getting the json file from client
    content = request.get_json()

    unique_id = Login.get_fast_id(content["username"])

    # previous information
    in_user = instaUsers_db.get_user(db, unique_id, instaUsers_db.col_unique_id)
    letter["previous_post_num"] = in_user.postsCount
    letter["previous_follower_num"] = in_user.folrs_count
    letter["previous_following_num"] = in_user.folng_count

    # new Informations
    new_inf = Login.get_public_informations(content["username"])
    letter["post_num"] = new_inf["post_num"]
    letter["follower_num"] = new_inf["follower_num"]
    letter["following_num"] = new_inf["following_num"]
    letter["bio"] = new_inf["bio"]
    letter["img_url"] = new_inf["img_url"]
    letter["name"] = new_inf["name"]

    # updating database
    editing_insta_user = instaUsers_db.get_user(db, unique_id, instaUsers_db.col_unique_id)
    editing_insta_user.postsCount = new_inf["post_num"]
    editing_insta_user.folrs_count = new_inf["follower_num"]
    editing_insta_user.folng_count = new_inf["following_num"]
    editing_insta_user.bio = new_inf["bio"]
    editing_insta_user.img_url = new_inf["img_url"]
    editing_insta_user.fullName = new_inf["name"]

    instaUsers_db.update_user(db, editing_insta_user)

    letter["response"] = mutual.success_process

    return jsonify(letter)


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
            "response": mutual.unknown_error
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
    print("........ db connected successfully ........")
    app.run()
