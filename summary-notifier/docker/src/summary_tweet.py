import boto3
import logging
import pprint
import os
import json
import gspread
from gspread.exceptions import *
import tweepy
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
from twitter_text import parse_tweet
import time
import collections

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
IMAGE_WIDTH = os.environ["IMAGE_WIDTH"]
IMAGE_HEIGHT = int(os.environ["IMAGE_HEIGHT"])
LIST_COUNT = int(os.environ["LIST_COUNT"])
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
    logging.info(workbook.lastUpdateTime)

    event_type = event["type"]
    if event_type == "summary":
        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('friend_competition')

        response = table.get_item(Key={"competition_name": workbook.lastUpdateTime})
        if "Item" in response:
            logging.info("スプレッドシートの更新がありません")
            if IS_TWEET == "on":
                result = api.update_status("本日は大会の更新がありません")
                return

        compe_day = []
        compe_time = []
        compe_name = []
        compe_rule = []
        compe_person = []
        compe_rule_detail = []
        compe_url = []
        compe_id = []
        compe_day_search = []
        compe_description = []
        compe_prize = []

        hash_tag = []
        now = datetime.now()

        day_records = {}
        for i in range(0, 60):
            notice_day = (now + timedelta(days=i))
            try:
                if notice_day.strftime("%Y%m") not in day_records:
                    day_records[notice_day.strftime("%Y%m")] = get_worksheet(workbook, notice_day.strftime("%Y%m")).get_all_records()
            except WorksheetNotFound:
                logging.warn("ワークシートが見つかりませんでした")
                break


        paging = [0]
        page = IMAGE_HEIGHT - 130 - 130 - 32
        for i in range(0, 60):
            notice_day = (now + timedelta(days=i))
            if notice_day.strftime("%Y%m") not in day_records:
                break
            for record in day_records[notice_day.strftime("%Y%m")]:
                if record["日付"] == notice_day.strftime("%Y/%m/%d"):
                    compe_day.append("{}({})".format(record["日付"], record["曜日"]))
                    compe_day_search.append(record["日付"].replace("/", "-"))
                    compe_time.append("{}-{}".format(record["開始（時）"], record["終了（時）"]))
                    compe_name.append("{}".format(record["大会名"]))
                    compe_rule.append("{}-{}".format(record["ルール"], record["シングル / ダブル"]))
                    # compe_person.append("{}({})".format(record["主催者名"], record["主催者 Twitter ユーザー名"]))
                    compe_person.append("{}".format(split_person(record["主催者名"], record["主催者 Twitter ユーザー名"])))
                    compe_rule_detail.append("{}".format(record["ルール縛り有無"]))
                    compe_description.append("{}".format(split_description(record["ルール詳細"])))
                    # compe_url.append("{}".format(record["ルール URL"]))
                    compe_id.append("{}".format(record["大会ID"]))
                    compe_prize.append("{}".format(record["景品"]))
                    logging.info(record)

                    hash_tag.append(record["ハッシュタグ"])

                    compe_person_br_count = (compe_person[-1].count("<br>") * 15) + 30
                    compe_description_br_count = (compe_description[-1].count("<br>") * 15) + 30

                    height = compe_description_br_count
                    if compe_person_br_count > compe_description_br_count:
                        height = compe_person_br_count

                    if (page - height) <= 0:
                        paging.append(len(compe_day))
                        page = IMAGE_HEIGHT - 130 - 130 - 32
                    page -= height

        if paging[-1] < len(compe_day):
            paging.append(len(compe_day))
        else:
            page = 0

        #祝日取得
#         s3 = boto3.resource('s3')
#         bucket = s3.Bucket("holiday-file-bucket")
#         obj = bucket.Object("holiday.json")
#
#         response = obj.get()
#         body = response['Body'].read()
#         holiday = json.loads(body.decode('utf-8'))
        holiday = {}

        compe_count = len(compe_day)
        media_ids = []        
        for i in range(0, len(paging) - 1):
            start = paging[i]
            end = paging[i + 1]
            
            #Dataframeの作成
            df = pd.DataFrame({"<b>日付</b>":compe_day[start:end], "<b>時間</b>":compe_time[start:end], "<b>大会名</b>":compe_name[start:end], "<b>ルール</b>":compe_rule[start:end], "<b>大会ID</b>": compe_id[start:end], "<b>主催者</b>":compe_person[start:end], "<b>ルール縛り</b>":compe_rule_detail[start:end], "<b>ルール詳細</b>":compe_description[start:end], "<b>景品</b>":compe_prize[start:end]})
            text_color = []
            col_text_color = []
            fill_color = []
            for j in range(start, end):
                compe_day_check = compe_day[j]
                if "土" in compe_day_check:
                    col_text_color.append("blue")
                elif "日" in compe_day_check:
                    col_text_color.append("red")
                elif compe_day_search[j] in holiday:
                    col_text_color.append("red")
                else:
                    col_text_color.append("black")
            text_color.append(col_text_color)
            text_color.append(["black"] * len(compe_day[start:end]))
            text_color.append(["black"] * len(compe_day[start:end]))
            text_color.append(["black"] * len(compe_day[start:end]))
            text_color.append(["black"] * len(compe_day[start:end]))
            text_color.append(["black"] * len(compe_day[start:end]))
            text_color.append(["black"] * len(compe_day[start:end]))
            text_color.append(["black"] * len(compe_day[start:end]))
            text_color.append(["black"] * len(compe_day[start:end]))

            fill_color.append(["white"] * len(compe_day[start:end]))
            fill_color.append(["white"] * len(compe_day[start:end]))
            fill_color.append(["white"] * len(compe_day[start:end]))
            fill_color.append(["white"] * len(compe_day[start:end]))
            fill_color.append(["white"] * len(compe_day[start:end]))
            fill_color.append(["white"] * len(compe_day[start:end]))
            col_fill_color = []
            for j in range(start, end):
                    compe_rule_detail_check = compe_rule_detail[j]
                    if "無" in compe_rule_detail_check:
                        col_fill_color.append("rgb(216, 216, 216)")
                    else:
                        col_fill_color.append("white")
            fill_color.append(col_fill_color)
            fill_color.append(["white"] * len(compe_day[start:end]))
            fill_color.append(["white"] * len(compe_day[start:end]))

            #テーブルの作成
            fig = go.Figure(data=[go.Table(
                    columnwidth =  [15, 15, 40, 25, 15, 30, 15, 60, 15], #カラム幅の変更
                    header=dict(values=df.columns, line_color='darkslategray', fill_color='rgb(216, 255, 255)', align='center', font_size=15),
                    cells=dict(
                        values=df.values.T,
                        line_color='darkslategray',
                        fill_color=fill_color,
                        align='left',
                        height=30,
                        # font_size=12
                        font=dict(color=text_color, size=12, family="IPAPGothic"),
                        )
                        )
                    ])
            # fig.update_layout(title={'text': "sample_table",'y':0.85,'x':0.5,'xanchor': 'center'})#タイトル位置の調整
            # fig.layout.title.font.size= 24 
            # fig.write_image("sample_table.jpg")
            # client = boto3.client('s3')
            # s3.Bucket("competition-image-bucket").upload_file('sample_table.jpg', 'sample_table.jpg')
            
#             obj = s3.Object("competition-image-bucket", "sample_table{}.png".format(start))

            # test_json = {'key': 'value'}
            if i == (len(paging) - 2):
                height = IMAGE_HEIGHT - page
            else:
                height = IMAGE_HEIGHT
            logging.info("image height: {}".format(height))
            image = fig.to_image(format="png", width=int(IMAGE_WIDTH), height=int(height))
#             r = obj.put(Body = image)
            media_upload_result = api.media_upload("list{}.png".format(start), file=BytesIO(image))
            logging.info(media_upload_result)
            media_ids.append(media_upload_result.media_id)

        # if IS_TWEET != "on":
        #     logging.info("ツイートオフなのでここで終了します")
        #     return
        logging.info(now.strftime("%w"))
        if now.strftime("%w") == "1":
            next_tweet_day = (now + timedelta(days=3))
        elif now.strftime("%w") == "4":
            next_tweet_day = (now + timedelta(days=4))
        else:
            next_tweet_day = (now + timedelta(days=7))

        tweet_head = "近日開催予定の仲間大会一覧です \n\nWeb版はプロフのURLからご確認ください" #Web版はこちら https://friendly-competition.net\n\n"
        tweet_last = "\n（リプライに続きます）"
        tweet_continue = "（続き）\n"

        first_tweet_hash_tag = ""
        tweet_hash_tag = ""
        is_first_tweet = True
        result = None
        for tag, v in collections.Counter(hash_tag).items():
            if is_first_tweet and parse_tweet("{}{}{}".format(tweet_head, first_tweet_hash_tag + tag + "\n", tweet_last)).asdict()["valid"] == False:
                # ツイート処理
                tweet_contents = "{}{}{}".format(tweet_head, first_tweet_hash_tag, tweet_last)
                logging.info(tweet_contents)
                is_first_tweet = False
                if IS_TWEET == "on":
                    result = api.update_status(status = tweet_contents, media_ids = media_ids)
                    logging.info(result)
                time.sleep(10)
            #     tweet_hash_tag = tag + "\n"
            # elif is_first_tweet and len(tag) > 0:
            #     first_tweet_hash_tag = first_tweet_hash_tag + tag + "\n"
            elif is_first_tweet == False and parse_tweet("{}{}".format(tweet_continue, tweet_hash_tag + tag + "\n")).asdict()["valid"] == False:
                # ツイート処理
                tweet_contents = "{}{}".format(tweet_continue, tweet_hash_tag)
                logging.info(tweet_contents)
                if IS_TWEET == "on":
                    result = api.update_status(status = tweet_contents, in_reply_to_status_id = result.id)
                    logging.info(result)
                time.sleep(10)
                # ハッシュタグリセット
                tweet_hash_tag = tag + "\n"
            elif is_first_tweet == False and len(tag) > 0:
                tweet_hash_tag = tweet_hash_tag + tag + "\n"
            
        # 残りがあったらツイート
        if is_first_tweet: # and len(first_tweet_hash_tag) > 0:
            tweet_contents = "{}{}".format(tweet_head, first_tweet_hash_tag)
            logging.info(tweet_contents)
            if IS_TWEET == "on":
                result = api.update_status(status = tweet_contents, media_ids = media_ids)
                logging.info(result)
        elif len(tweet_hash_tag) > 0:
            tweet_contents = "{}{}".format(tweet_continue, tweet_hash_tag)
            logging.info(tweet_contents)
            if IS_TWEET == "on":
                result = api.update_status(status = tweet_contents, in_reply_to_status_id = result.id)
                logging.info(result)

        response = table.put_item(Item={"competition_name": workbook.lastUpdateTime})

    else:
        logging.info("実行する処理がありません")
    return

def split_description(description):
    result = []
    for d in description.split("。"):
        v = [d[i: i + 35] for i in range(0, len(d), 35)]
        result.extend(v)
    logging.info(result)
    if len(result) == 0:
        return description
    return "<br>".join(result)

def split_person(person, name):
    person_result = person.split(" ")
    name_result = name.split(" ")
    logging.info(person_result)
    logging.info(name_result)
    person_and_name_result = []
    for i in range(0, len(person_result)):
        person_and_name_result.append("{}({})".format(person_result[i], name_result[i])) 
    return "<br>".join(person_and_name_result)

def connect_gspread(jsonf, key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(key)

def get_worksheet(gc, worksheet):
    return gc.worksheet(worksheet)
