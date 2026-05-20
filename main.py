import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tweepy
import os

URL = "https://ticketdive.com/event/UJymXUNRtuGGD0w5LGLX"

client = tweepy.Client(
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_SECRET"]
)

html = requests.get(URL).text

soup = BeautifulSoup(html, "html.parser")
text = soup.get_text("\n")

pattern = r'抽選[^\n]*?～.*?(\d{1,2})月(\d{1,2})日'

match = re.search(pattern, text)

if match:

    month, day = map(int, match.groups())

    now = datetime.now()

    if now.month == month and now.day == day:

        post_text = f"""
【本日締切】

抽選受付は本日締切です！

{URL}
"""

        client.create_tweet(text=post_text)

        print("投稿完了")

    else:
        print("今日は締切ではありません")