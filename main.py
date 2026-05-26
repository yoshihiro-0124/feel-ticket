import re
import requests
from bs4 import BeautifulSoup
import tweepy
import os

# =====================
# TicketDive URL一覧
# =====================

URLS = [
    "https://ticketdive.com/event/UJymXUNRtuGGD0w5LGLX"
]

# =====================
# X API設定
# =====================

client = tweepy.Client(
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_SECRET"]
)

# =====================
# URLを順番に確認
# =====================

for URL in URLS:

    try:

        # =====================
        # ページ取得
        # =====================

        html = requests.get(URL).text

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text("\n")

        # =====================
        # 抽選締切取得
        # =====================

        pattern = r'抽選受付中.*?(\d{4})\/(\d{2})\/(\d{2}).*?〜.*?(\d{4})\/(\d{2})\/(\d{2})'

        match = re.search(pattern, text, re.DOTALL)

        if match:

            start_year, start_month, start_day, \
            end_year, end_month, end_day = match.groups()

            month = int(end_month)
            day = int(end_day)

            # =====================
            # 投稿文作成
            # =====================

            post_text = f"""
抽選受付の締切は
{month}月{day}日です！

{URL}

#ライブ
#チケット
"""

            # =====================
            # X投稿
            # =====================

            client.create_tweet(text=post_text)

            print(f"投稿完了: {URL}")

        else:

            print(f"抽選情報が見つかりません: {URL}")

    except Exception as e:

        print(f"エラー: {URL}")

        print(e)
