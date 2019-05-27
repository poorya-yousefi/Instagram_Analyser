



def clean_list( filename):
    def openfile(filename):
        open_file = open("/root/Desktop/py/hemin1/" + filename +"followers.txt", "r+")
        read = open_file.read()
        return read
        open_file.close()


    read = openfile(filename)
    re = read.replace("'https://www.instagram.com/", "")
    me = re.replace("/'", "")
    de = me.replace(" ", "\n")
    he = open("/root/Desktop/py/hemin1clean/" + filename + "clean.txt", "w+")
    he.write(de)
    he.close()


file = open("/root/Desktop/py/clean/hemin.saedfollowersclean (copy).txt")
mm = file.readlines()
for i in range(200):

    a = mm[i].replace("[", "")
    b = a.replace("]", "")

    c = b.replace(",", "")
    me = c.replace("/'", "")

    de = me.replace("\n","")
    print(de)
    clean_list(de)