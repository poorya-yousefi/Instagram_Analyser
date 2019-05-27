import requests


url = "https://www.instagram.com/guilan.fanni/"
r = requests.get(url)
print(r.text)

