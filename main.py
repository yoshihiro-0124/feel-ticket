import re
import requests
from bs4 import BeautifulSoup
import tweepy
import os

URLS = [
    "https://ticketdive.com/event/feelneo-nexttour0719"
]

client = tweepy.Client(
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_SECRET"]
)

for URL in URLS:

    try:

        html = requests.get(URL).text

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text("\n")

        # =====================
        # 日付取得
        # =====================

        pattern = r'(\d{4})\/(\d{2})\/(\d{2})'

        matches = re.findall(pattern, text)

        if matches:

            # 最後の日付を締切として使う
            year, month, day = matches[-1]

            # 先頭の0を消す
            month = int(month)
            day = int(day)

            # =====================
            # 投稿文
            # =====================

            post_text = f"""
抽選受付の締切は
{month}月{day}日 です！

{URL}

#ライブ
#チケット
"""

            client.create_tweet(text=post_text)

            print(f"投稿完了: {URL}")

        else:

            print(f"日付が見つかりません: {URL}")

    except Exception as e:

        print(f"エラー: {URL}")
        print(e)
