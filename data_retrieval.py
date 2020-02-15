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


# Get stock prices based on events.json
def get_stock_prices(events):
    stock_data = []
    for event in events["events"]:
        tmp = DataReader("TSLA", "yahoo", event["event_start"], event["event_end"])
        stock_data.append(tmp)
    return pd.concat(stock_data)


# Handle rate-limit of TwitterAPI
def limit_handler(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


# Get Twitter data based on events.json
def get_twitter_data(events):
    CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    query = ''
    for i in argv[2:]:
        query += i
        query += ' '

    # results = api.search(q="#cybertruck #teslacybertruck", since='19-10-2019', until='24-10-2019', lang='en')
    results = []
    for items in limit_handler(tweepy.Cursor(api.search, q=query, since=argv[0], until=argv[1], lang="en").items(100)):
        results.append(items)

    results_json = json.dumps(results)

    with open('data.txt', 'w') as outfile:
        json.dump(results_json, outfile)


def main():
    events = read_events()
    stock_prices = get_stock_prices(events)


if __name__ == "__main__":
    main()
