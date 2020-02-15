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
        stock_price = DataReader(events["stock"], "yahoo", event["event_start"], event["event_end"])
        stock_price.to_csv("stocks/" + event["event_start"] + "_" + event["event_end"] + ".csv")


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
    CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    for event in events["events"]:
        tweets = { "tweets": [] }
        # TODO: Check if date format is readable from TwitterAPI?
        # Check http://docs.tweepy.org/en/latest/api.html
        for items in limit_handler(tweepy.Cursor(api.search, q=event["hashtags"], since=event["event_start"], until=event["event_end"], lang="en").items()):
            tweets["tweets"].append(items)

        # Got all event data - write them to file
        tweets_json = json.dumps(tweets)
        with open("tweets/" + event["event_start"] + "_" + event["event_end"] + ".json", 'w') as outfile:
            json.dump(tweets_json, outfile)


def main():
    events = read_events()
    # get_twitter_data(events)
    # get_stock_prices(events)


if __name__ == "__main__":
    main()
