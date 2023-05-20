import logging
import pprint
import os
import json
import tweepy
from datetime import date, datetime, timezone, timedelta
import re
from twitter_text import parse_tweet
import textwrap

logger = logging.getLogger()
logger.setLevel(logging.INFO)
pp = pprint.PrettyPrinter(indent=4)

TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
IS_TWEET = os.environ["IS_TWEET"]

def lambda_handler(event, context):
    logging.info("<event>: \n" + json.dumps(event))

    if IS_TWEET == "on":
        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        # ツイート内容変更はここを修正する
        tweet_contents = textwrap.dedent('''\
        [定期ツイート]
        仲間大会参加準備はお済みですか❓

        ✅仲間大会確認
        　☑️大会エントリー
        　☑️ルール確認

        ✅ポケモン準備
        　☑️チーム編成
        　☑️レベル
        　☑️技構成・PP
        　☑️持ち物
        　☑️特性
        　☑️努力値
        　☑️固体値
        　☑️ニックネーム
        　☑️ダイマLv/ダイスープ
        　☑️バトルレギュレーションマーク
        ''')
        if parse_tweet(tweet_contents).asdict()["valid"] == True:
            result = api.update_status(status = tweet_contents)
            logging.info(result)
