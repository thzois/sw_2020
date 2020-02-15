from dotenv import load_dotenv
load_dotenv()

from pandas_datareader.data import DataReader
import pandas as pd
import tweepy

import json
import sys
import os


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


# Get Twitter data based on events.json and store 
# them in separate files based on the event dates
def get_twitter_data(events):
    CONSUMER_KEY = os.getenv("TWITTER_API_KEY")
    CONSUMER_SECRET = os.getenv("TWITTER_API_SECRET")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    for event in events["events"]:
        tweets = { "tweets": [] }
        # TODO: Check if date format is readable from TwitterAPI?
        # Check http://docs.tweepy.org/en/latest/api.html
        for items in limit_handler(tweepy.Cursor(api.search, q=event["hashtags"], since=event["start_date"], until=event["end_date"], lang="en").items()):
            tweets["tweets"].append(items)

        # Got all event data - write them to file
        tweets_json = json.dumps(tweets)
        with open("tweets/" + event["start_date"] + "_" + event["end_date"] + ".json", 'w') as outfile:
            json.dump(tweets_json, outfile)


def main():
    events = read_events()
    # get_twitter_data(events)
    # get_stock_prices(events)


if __name__ == "__main__":
    main()
