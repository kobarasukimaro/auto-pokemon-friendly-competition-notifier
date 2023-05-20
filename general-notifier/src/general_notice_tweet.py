import boto3
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

TWITTER_CONSUMER_KEY_SSM_PARAM_NAME = os.environ["TWITTER_CONSUMER_KEY_SSM_PARAM_NAME"]
TWITTER_CONSUMER_SECRET_SSM_PARAM_NAME = os.environ["TWITTER_CONSUMER_SECRET_SSM_PARAM_NAME"]
TWITTER_ACCESS_TOKEN_SSM_PARAM_NAME = os.environ["TWITTER_ACCESS_TOKEN_SSM_PARAM_NAME"]
TWITTER_ACCESS_TOKEN_SECRET_SSM_PARAM_NAME = os.environ["TWITTER_ACCESS_TOKEN_SECRET_SSM_PARAM_NAME"]
IS_TWEET = os.environ["IS_TWEET"]

def lambda_handler(event, context):
    logging.info("<event>: \n" + json.dumps(event))

    if IS_TWEET == "on":
        TWITTER_CONSUMER_KEY = get_parameter(TWITTER_CONSUMER_KEY_SSM_PARAM_NAME)
        TWITTER_CONSUMER_SECRET = get_parameter(TWITTER_CONSUMER_SECRET_SSM_PARAM_NAME)
        TWITTER_ACCESS_TOKEN = get_parameter(TWITTER_ACCESS_TOKEN_SSM_PARAM_NAME)
        TWITTER_ACCESS_TOKEN_SECRET = get_parameter(TWITTER_ACCESS_TOKEN_SECRET_SSM_PARAM_NAME)

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

def get_parameter(parameter_name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=True
    )

    # Get parameter value
    param_value = response['Parameter']['Value']

    return param_value