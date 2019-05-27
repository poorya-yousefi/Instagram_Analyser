import instaloader
L = instaloader.Instaloader()

# Login or load session
L.login("rhino_handmade", "mrbot911")        # (login)

print("login")

def get_net(filename):
    # Obtain profile metadata
    filel = open("/root/Desktop/py/clean/" + filename + ".txt")
    mm = filel.readlines()
    # print(str(mm))
    for i in range(0, int(mm[-1])):
        a = mm[i].replace("[", "")
        b = a.replace("]", "")
        c = b.replace(",", "")
        d= c.replace("\n","")
        profile = instaloader.Profile.from_username(L.context,d)
        if int(profile.followers) <= int(1000):
            print(d)
            file = open("/root/Desktop/py/api/" + d + "followers.txt", "a+")
            follow_list = []
            count = 0
            for followee in profile.get_followers():
                follow_list.append(followee.username)
                file.write(follow_list[count])
                file.write("\n")
                print(count,follow_list[count])
                count = count + 1
    file.close()
    filel.close()

# print(profile.get_followees())
# Print list of followees
get_net("rhino_handmadeclean")




