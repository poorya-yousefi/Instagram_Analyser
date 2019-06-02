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
    result = {
        "response": ""
    }
    if not request.is_json:
        letter["response"] = mutual.unknown_error
        return jsonify(letter)
    else:
        # getting the json file from client
        content = request.get_json()

        # getting the unique id for searching the database
        unique_id = Login.get_fast_id(content["username"])

        print("There was a request for username " + content["username"] + " with unique id " + unique_id + " . ")

        # checking for existing user
        if instaUsers_db.get_user(db, unique_id, instaUsers_db.col_unique_id) is not None:
            if appUsers_db.get_user(db, unique_id) is not None:
                result["response"] = mutual.existing_user
                print(
                    "There was an existing user for instaUser and AppUser with unique id " + unique_id +
                    " and username " + instaUsers_db.get_user(
                        db, unique_id, instaUsers_db.col_unique_id).instaId)
                return jsonify(result)
            # if we have an instaUser just make an app user
            else:
                print(
                    "There was an existing user for instaUser  with unique id " + unique_id +
                    " and username " + instaUsers_db.get_user(
                        db, unique_id, instaUsers_db.col_unique_id).instaId)

                new_app_user = appUser.CommercialUser(unique_id, datetime.datetime.now(), False, content["country"],
                                                      content["city"],
                                                      content["phone_num"], content["personality_key_words"], "", "",
                                                      content["company_name"], content["activity"])
                appUsers_db.insert_user(db, new_app_user)

                print("DataBase is created (just appUser) was created for the user with username "
                      " " + content["username "] + " and unique id " + unique_id + " . ")

                # trying to login to the page to see can we login or not
                try:
                    user = Login.Login(content["username"], content["password"])
                    result = user.login()
                except Exception:
                    print("Some Error in selenium for signing up for user with uername " + content[
                        "username"] + "and with unique id " + unique_id + ".")
                    result["response"] = mutual.selenium_error
                    return result

                # check that can we log as a username or not
                try:
                    user = Login.Login(content["username"], content["password"])
                    result = user.login()
                except Exception:
                    print("Some Error in selenium for signing up for user with uername " + content[
                        "username"] + "and with unique id " + unique_id + ".")
                    result["response"] = mutual.selenium_error
                    return result

                if result["response"] is mutual.incorrect_pass:
                    print("There was an attempt for signing up for username " + content[
                        "username"] + " with unique id : " + unique_id +
                          " , but the password was incorrect .(existing instauser fpr this acount )")
                    return jsonify(result)
                elif result["response"] is mutual.two_step_en:
                    print("There was an attempt for signing up for username " + content[
                        "username"] + " with unique id : " + unique_id + " but it has two step verification code"
                                                                         ". (existing instauser fpr this account )")
                    dic["user"] = user
                    return jsonify(result)
                return jsonify(result)
        # trying to login to the page to see can we login or not
        # check that can we log as a username or not
        try:
            user = Login.Login(content["username"], content["password"])
            result = user.login()
        except Exception:
            print("Some Error in selenium for signing up for user with uername " + content[
                "username"] + "and with unique id " + unique_id + ".")
            result["response"] = mutual.selenium_error
            return result

        if result["response"] is mutual.incorrect_pass:
            print("There was an attempt for signing up for username " + content[
                "username"] + " with unique id : " + unique_id +
                  " , but the password was incorrect .")
            return jsonify(result)
        elif result["response"] is mutual.two_step_en:
            print("There was an attempt for signing up for username " + content[
                "username"] + " with unique id : " + unique_id + " , but it has two step verification code.")
            dic["user"] = user
            return jsonify(result)

        if result["response"] == mutual.success_login:
            print("A success sign up for " + content["username"] + ". ")

            if content["page_type"] == mutual.commercial_user:
                user_information = Login.get_public_informations(content["username"])
                new_insta_user = instaUser.InstaUser(content["username"], unique_id,
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

                print("Data base was just created (both appUser and instaUser) for the user with username " + content[
                    "username"] + " with uniqueID " + unique_id)

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
    print()
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
    result = {
        "response": ""
    }

    if request.is_json:

        content = request.get_json()
        # Getting the fast id (unique id) to search with data base.
        unique_id = Login.get_fast_id(content["username"])

        print("A login request received from user with username : " + content[
            "username"] + " and uniqueID : " + unique_id + " . ")

        # search for the login requested user to see there is an existing account or not
        user = appUsers_db.get_user(db, unique_id)

        # if there is no existing account for user , return the related error
        if user is None:
            print("There were no sign up for the user with username : " + content[
                "username"] + " and uniqueID : " + unique_id + " . ")
            result["response"] = mutual.no_sign_up
            return jsonify(result)

        try:
            # log in to the page with selenium
            user = Login.Login(content["username"], content["password"])
            result = user.login()
            dic["user"] = user
        except Exception:
            print("Some Error in selenium for signing up for user with uername " + content[
                "username"] + "and with unique id " + unique_id + ".")
            result["response"] = mutual.selenium_error
            return result

        # checking the error of information that user entered
        if result["response"] is mutual.two_step_en:
            print("Trying to login for the user with username : " + content[
                "username"] + " and uniqueID : " + unique_id + " . ")
            return jsonify(result)
        elif result["response"] is mutual.incorrect_pass:
            return jsonify(result)



    else:
        result = {
            "response": mutual.unknown_error
        }
        return jsonify(result)


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

        unique_id = Login.get_fast_id(content["username"])

        if result["response"] == mutual.success_login:
            user_information = Login.get_public_informations(content["username"])
            new_insta_user = instaUser.InstaUser(content["username"], unique_id,
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
        return result['response']
    else:
        letter = {
            "response": mutual.unknown_error
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
