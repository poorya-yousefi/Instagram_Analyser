import requests

url = 'https://www.instagram.com/prada'
r = requests.get(url).text
file = open("text.txt","w+")
file.write(r)
file.close()
print(r)
