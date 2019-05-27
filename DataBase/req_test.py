import requests
import instagram_scraper as insta

# url = "https://www.instagram.com/guilan.fanni/"
# r = requests.get(url)
# print(r.text)

s = insta.InstagramScraper.get_profile_info(dst="", username="guilan.fanni")
