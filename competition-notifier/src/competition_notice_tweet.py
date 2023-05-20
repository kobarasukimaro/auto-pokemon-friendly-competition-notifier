import boto3
import logging
import pprint
import os
import json
import gspread
from gspread.exceptions import *
import tweepy
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime, timezone, timedelta
import re
from twitter_text import parse_tweet

logger = logging.getLogger()
logger.setLevel(logging.INFO)
pp = pprint.PrettyPrinter(indent=4)

SPREAD_SHEET_KEY_SSM_PARAM_NAME = os.environ["SPREAD_SHEET_KEY_SSM_PARAM_NAME"]
GCP_KEY_SSM_PARAM_NAME = os.environ["GCP_KEY_SSM_PARAM_NAME"]
GCP_KEY_FILE_NAME = "gcp_key.json"

TWITTER_CONSUMER_KEY_SSM_PARAM_NAME = os.environ["TWITTER_CONSUMER_KEY_SSM_PARAM_NAME"]
TWITTER_CONSUMER_SECRET_SSM_PARAM_NAME = os.environ["TWITTER_CONSUMER_SECRET_SSM_PARAM_NAME"]
TWITTER_ACCESS_TOKEN_SSM_PARAM_NAME = os.environ["TWITTER_ACCESS_TOKEN_SSM_PARAM_NAME"]
TWITTER_ACCESS_TOKEN_SECRET_SSM_PARAM_NAME = os.environ["TWITTER_ACCESS_TOKEN_SECRET_SSM_PARAM_NAME"]
IS_TWEET = os.environ["IS_TWEET"]

def lambda_handler(event, context):
    logging.info("<event>: \n" + json.dumps(event))

    SPREAD_SHEET_KEY = get_parameter(SPREAD_SHEET_KEY_SSM_PARAM_NAME)
    GCP_KEY = get_parameter(GCP_KEY_SSM_PARAM_NAME)
    f = open(GCP_KEY_FILE_NAME, 'w')
    f.write(GCP_KEY)
    f.close()
    TWITTER_CONSUMER_KEY = get_parameter(TWITTER_CONSUMER_KEY_SSM_PARAM_NAME)
    TWITTER_CONSUMER_SECRET = get_parameter(TWITTER_CONSUMER_SECRET_SSM_PARAM_NAME)
    TWITTER_ACCESS_TOKEN = get_parameter(TWITTER_ACCESS_TOKEN_SSM_PARAM_NAME)
    TWITTER_ACCESS_TOKEN_SECRET = get_parameter(TWITTER_ACCESS_TOKEN_SECRET_SSM_PARAM_NAME)

    workbook = connect_gspread(GCP_KEY_FILE_NAME, SPREAD_SHEET_KEY)

    # lambda url 対応
    if "queryStringParameters" in event:
        event_type = event["queryStringParameters"]["type"]
    else:
        event_type = event["type"]

    if event_type == "tweet":
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('friend_competition')
        # tokyo_tz = datetime.timezone(timedelta(hours=9))
        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        JST = timezone(timedelta(hours=+9))
        now = datetime.now(JST)
        tomorrow = (now + timedelta(days=1))
        end_process = False

        day_records = {}
        for i in range(0, 7):
            notice_day = (now + timedelta(days=i))
            try:
                if notice_day.strftime("%Y%m") not in day_records:
                    day_records[notice_day.strftime("%Y%m")] = get_worksheet(workbook, notice_day.strftime("%Y%m")).get_all_records()
            except WorksheetNotFound:
                logging.warn("ワークシートが見つかりませんでした")
                break

        for i in range(0, 7):
            notice_day = (now + timedelta(days=i))
            if notice_day.strftime("%Y%m") not in day_records:
                break
            for record in day_records[notice_day.strftime("%Y%m")]:
                if record["日付"] == notice_day.strftime("%Y/%m/%d"):
                    logging.info(record)
                    response = table.get_item(Key={"competition_name": record["日付"] + record["大会名"]})
                    if "Item" in response:
                        logging.info(record["日付"] + record["大会名"] + " はすでにツイートされているのでスキップします")
                        continue

                    if record["入力完了"] == "未":
                        logging.info(record["大会名"] + " は入力状態が" + record["入力完了"] + " のためスキップします")
                        continue

                    compe_day = "{}({})に".format(record["日付"], record["曜日"])
                    tweet_contents = "{}開催する{}の情報をお知らせします {}\n{}".format(compe_day, record["大会名"], record["ハッシュタグ"], record["ルール URL"])
                    logging.info(tweet_contents)

                    if "一言" in record and len(record["一言"]) > 0:
                        words_tweet = "{}\n{}".format(tweet_contents, record["一言"])
                        if parse_tweet(words_tweet).asdict()["valid"] == True:
                            tweet_contents = words_tweet

                    if IS_TWEET == "on":
                        result = api.update_status(status = tweet_contents)
                        logging.info(result)

                        if record["当日追加"] == "追加":
                            compare_start_time = record["開始（時）"]
                            if record["日付"] == now.strftime("%Y/%m/%d") or (record["日付"] == tomorrow.strftime("%Y/%m/%d") and compare_start_time < "13:00"):
                                daily_tweet_date = now.strftime("%Y%m%d")
                                if record["日付"] == tomorrow.strftime("%Y/%m/%d"):
                                    daily_tweet_date = tomorrow.strftime("%Y%m%d")

                                daily_tweet_table = dynamodb.Table("daily_tweet")
                                response = daily_tweet_table.get_item(Key={"date": daily_tweet_date})
                                if "Item" in response:
                                    if len(compare_start_time) == 4:
                                        compare_start_time = "0" + compare_start_time
                                    tweet_contents = "本日開催予定の大会の追加情報です\nhttps://mobile.twitter.com/fri_comp_info/status/{}".format(result.id)
                                    result = api.update_status(status = tweet_contents, in_reply_to_status_id = response["Item"]["in_reply_to_status_id"])
                                    logging.info(result)

                    response = table.put_item(Item={"competition_name": record["日付"] + record["大会名"]})

                    end_process = True
                    break
            if end_process:
                break
    elif event_type == "retweet":
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('friend_competition')
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        now = datetime.now()
        end_process = False

        day_records = {}
        for i in range(8, 60):
            notice_day = (now + timedelta(days=i))
            try:
                if notice_day.strftime("%Y%m") not in day_records:
                    day_records[notice_day.strftime("%Y%m")] = get_worksheet(workbook, notice_day.strftime("%Y%m")).get_all_records()
            except WorksheetNotFound:
                logging.warn("ワークシートが見つかりませんでした")
                break

        for i in range(8, 60):
            notice_day = (now + timedelta(days=i))
            if notice_day.strftime("%Y%m") not in day_records:
                break
            for record in day_records[notice_day.strftime("%Y%m")]:
                if record["日付"] == notice_day.strftime("%Y/%m/%d"):
                    logging.info(record)

                    if record["リツイート用"] == "":
                        logging.info(record["大会名"] + " はリツイート用URLが空のためスキップします")
                        continue

                    response = table.get_item(Key={"competition_name": record["リツイート用"]})
                    if "Item" in response:
                        logging.info(record["リツイート用"] + " はすでにリツイートされているのでスキップします")
                        continue

                    if record["入力完了"] == "未":
                        logging.info(record["大会名"] + " は入力状態が" + record["入力完了"] + " のためスキップします")
                        continue

                    m = re.search('.+/status\/(\d+)\?', record["リツイート用"])
                    status_id = m.group(1)
                    print(status_id)

                    if re.match("^[0-9]+$", status_id) is None:
                        logging.info(status_id + "tweet の id 表記ではないためスキップします")
                        continue

                    if IS_TWEET == "on":
                        try:
                            result = api.retweet(int(status_id))
                            logging.info(result)
                        except tweepy.TweepError as e:
                            logging.warn(e.response)
                            logging.warn("tweepy エラーのためスキップします")
                            continue


                    response = table.put_item(Item={"competition_name": record["リツイート用"]})
                    end_process = True
                    break
            if end_process:
                break

def connect_gspread(jsonf, key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(key)

def get_worksheet(gc, worksheet):
    return gc.worksheet(worksheet)

def get_parameter(parameter_name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=True
    )

    # Get parameter value
    param_value = response['Parameter']['Value']

    return param_value