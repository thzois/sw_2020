from dotenv import load_dotenv
load_dotenv()

from pandas_datareader.data import DataReader
import pandas as pd
import tweepy

import json
import sys
import os
import time
import datetime


# read events.json 
def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


# get stock prices based on events.json and store 
# them to separate files based on the event dates
def get_stock_prices(events):
    for event in events["events"]:
        stock_price = DataReader(events["stock"], "yahoo", event["start_date"], event["end_date"])
        stock_price.to_csv("stocks/" + event["start_date"] + "_" + event["end_date"] + ".csv")


# handle rate-limit of TwitterAPI
def limit_handler(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
        except tweepy.TweepError as e:
            if e.response is not None and (e.response.status == 420 or e.response.status == 429):
                time.sleep(15 * 60)
            else:
                print("Break due to exception: ", e)
                break
        except StopIteration:
            break


# get Twitter data based on events.json and store 
# them in separate files based on the event dates
def get_twitter_data(events):
    API_KEY = os.getenv("TWITTER_API_KEY")
    API_SECRET = os.getenv("TWITTER_API_SECRET")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    TWITTER_APP_ENV = os.getenv("TWITTER_APP_ENV")

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    for event in events["events"]:
        # prepare query string
        # see: https://developer.twitter.com/en/docs/tweets/rules-and-filtering/guides/using-premium-operators
        query_string = "("
        for i in range (0, len(event["hashtags"])):
            if i == len(event["hashtags"]) - 1:
                query_string += event["hashtags"][i]
            else:
                query_string += event["hashtags"][i] + " OR "
        query_string += ") lang:en"

        # twitter premium API expects date to be in format 'yyyyMMddHHmm'
        start_datetime = event["start_date"].replace("-", "") + "0000"
        end_datetime = event["end_date"].replace("-", "") + "0000"
        tweets = { "tweets": [] }

        # tweepy docs: https://github.com/tweepy/tweepy/blob/premium-search/docs/api.rst
        # premium API does not support 'lang' but returns 
        for items in limit_handler(tweepy.Cursor(api.search_full_archive, environment_name=TWITTER_APP_ENV, query=query_string, fromDate=start_datetime, toDate=end_datetime).items()):
            tweets["tweets"].append(items._json)
        
        # got all event data - write them to file
        filename = event["start_date"] + "_" + event["end_date"] + ".json"
        with open("tweets/" + filename, 'w') as outfile:
            json.dump(tweets, outfile, ensure_ascii=True, indent=4)


def main():
    events = read_events()
    # get_twitter_data(events)
    # get_stock_prices(events)


if __name__ == "__main__":
    main()
