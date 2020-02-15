from dotenv import load_dotenv
load_dotenv()

from pandas_datareader.data import DataReader
import pandas as pd
import tweepy

import json
import sys
import os
import time


# Read events.json 
def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


# Get stock prices based on events.json and store 
# them to separate files based on the event dates
def get_stock_prices(events):
    for event in events["events"]:
        stock_price = DataReader(events["stock"], "yahoo", event["start_date"], event["end_date"])
        stock_price.to_csv("stocks/" + event["start_date"] + "_" + event["end_date"] + ".csv")


# Handle rate-limit of TwitterAPI
def limit_handler(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
        except StopIteration:
            break


# Get Twitter data based on events.json and store 
# them in separate files based on the event dates
def get_twitter_data(events):
    API_KEY = os.getenv("TWITTER_API_KEY")
    API_SECRET = os.getenv("TWITTER_API_SECRET")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    for event in events["events"]:
        # prepare query string - when using multiple hashtags ( #example OR #Example )
        query_string = ""
        for i in range (0, len(event["hashtags"])):
            if i == len(event["hashtags"]) - 1:
                query_string += event["hashtags"][i]
            else:
                query_string += event["hashtags"][i] + " OR "

        tweets = { "tweets": [] }
        for items in limit_handler(tweepy.Cursor(api.search, q=query_string, until=event["end_date"], lang="en", include_entities=True).items()):
            tweets["tweets"].append(items._json)

        # Got all event data - write them to file
        with open("tweets/" + event["start_date"] + "_" + event["end_date"] + ".json", 'w') as outfile:
            json.dump(tweets, outfile, ensure_ascii=True, indent=4)


def main():
    events = read_events()
    # get_twitter_data(events)
    # get_stock_prices(events)


if __name__ == "__main__":
    main()
