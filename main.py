import tweepy
import os

client = tweepy.Client(
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_SECRET"]
)

client.create_tweet(
    text="テスト投稿です。GitHub Actionsから自動投稿できています。"
)

print("投稿完了")
