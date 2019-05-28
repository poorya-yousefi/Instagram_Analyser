from flask import Flask
from flask import request
from flask import jsonify
from Server.Selenium import Login, Relations

app = Flask(__name__)

dic = {
    "user": None
}

# Common Errors
notJson = "Login Failed, The received file is not json."


@app.route("/first_page_info", methods=["GET", "Post"])
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


# @app.route("/get_follower", ["POST"])
# def get_followers_handler():
#     print()


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
        Relations.get_relations("iBotErfan")


    else:
        print(notJson)
        return notJson


@app.route("/getFollowing", methods=['POST'])
def get_following_list_handler():
    if request.is_json:
        print("Get following json is received")
        content = request.get_json()
        print("Get following json contents is : ", content)

        # getting the Login objects
        user = dic["user"]

        # saving objects to
        following = user.get_followers_list(content['username'], "following")
        return following

    else:
        print(notJson)
        return notJson

if __name__ == "__main__":
    app.run()
