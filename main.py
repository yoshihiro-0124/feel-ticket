import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tweepy
import os

# =====================
# URL一覧
# =====================

URLS = [
    "https://ticketdive.com/event/UJymXUNRtuGGD0w5LGLX",
    "https://ticketdive.com/event/x0GYEa3LVuk56WtUTXdm",
    "https://ticketdive.com/event/feelneo-nexttour0719"
]

# =====================
# X API
# =====================

client = tweepy.Client(
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_SECRET"]
)

# 今日の日付
now = datetime.now()

# =====================
# URLを順番に確認
# =====================

for URL in URLS:

    try:

        html = requests.get(URL).text

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text("\n")

        # =====================
        # 締切日抽出
        # =====================

        pattern = r'(\d{4})\/(\d{2})\/(\d{2}).*?23:59'

        matches = re.findall(pattern, text)

        if matches:

            # 最後の日付を締切として使う
            year, month, day = matches[-1]

            year = int(year)
            month = int(month)
            day = int(day)

            if (
                now.year == year and
                now.month == month and
                now.day == day
            ):

                post_text = f"""
【本日締切】

抽選受付は本日締切です！

{URL}

#feelNEO
"""

                client.create_tweet(text=post_text)

                print(f"投稿完了: {URL}")

            else:
                print(f"締切日ではない: {URL}")

        else:
            print(f"抽選情報なし: {URL}")

    except Exception as e:

        print(f"エラー: {URL}")
        print(e)
