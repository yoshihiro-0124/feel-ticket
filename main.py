import re
import requests
from bs4 import BeautifulSoup
import tweepy
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# =====================
# TicketDive URL一覧
# =====================

URLS = [
    "https://ticketdive.com/event/feelneo-nexttour0719"
]

# =====================
# 現在時刻（日本時間）
# =====================

now = datetime.now(ZoneInfo("Asia/Tokyo"))

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
        # イベントタイトル取得
        # =====================

        title_element = soup.find(
            "span",
            class_="Typography_root__axuOu EventInfoUnit_name__2GVAA"
        )

        if title_element:

            event_title = title_element.get_text(strip=True)

        else:

            event_title = "イベント"

        # =====================
        # 公演日時取得
        # =====================

        performance_date = "公演日時不明"

        performance_spans = soup.find_all(
            "span",
            class_="Typography_root__axuOu"
        )

        for span in performance_spans:

            span_text = span.get_text(strip=True)

            if "開場時刻" in span_text and "開演時刻" in span_text:

                performance_date = re.sub(
                    r'(\d{4}/\d{1,2}/\d{1,2}\(.+?\))',
                    r'\1\n',
                    span_text
                )

                break

        # =====================
        # 抽選締切取得
        # =====================

        pattern = r'抽選受付中.*?(\d{4})\/(\d{2})\/(\d{2}).*?〜.*?(\d{4})\/(\d{2})\/(\d{2}).*?(\d{2}:\d{2})'

        match = re.search(pattern, text, re.DOTALL)

        if match:

            (
                start_year,
                start_month,
                start_day,
                end_year,
                end_month,
                end_day,
                end_time
            ) = match.groups()

            deadline_year = int(end_year)
            deadline_month = int(end_month)
            deadline_day = int(end_day)

            # =====================
            # 締切日当日だけ投稿
            # =====================

            if (
                now.year == deadline_year and
                now.month == deadline_month and
                now.day == deadline_day
            ):

                # =====================
                # 投稿文作成
                # =====================

                post_text = f"""
【抽選受付締切は本日です】

{event_title}

■ 公演日時
{performance_date}

■ 抽選受付締切
{deadline_month}月{deadline_day}日 {end_time}

{URL}

#feelNEO
"""

                # =====================
                # X投稿
                # =====================

                client.create_tweet(text=post_text)

                print(f"投稿完了: {URL}")

            else:

                print(f"本日は締切日ではありません: {URL}")

        else:

            print(f"抽選情報が見つかりません: {URL}")

    except Exception as e:

        print(f"エラー: {URL}")

        print(e)
