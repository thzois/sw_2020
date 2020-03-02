import pandas as pd
import json
import csv
import sys
import os


def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


def stock_sent_day_normalized(events):
    for event in events["events"]:
        filename = event["start_date"] + "_" + event["end_date"]

        # normalize stocks
        stock_df = pd.read_csv("stocks/" + filename + ".csv")
        idx_max = stock_df["Adj Close"].idxmax()
        stock_df["Adj Close"] = stock_df["Adj Close"].div(stock_df.iloc[0]["Adj Close"])
        
        # stock_df.to_csv('../web-app/results/stocks/' + filename, index = False)
        with open("results_sa/" + filename + ".json", "r") as twitter_file:
            twitter_data = json.load(twitter_file)["tweets"]

            neg = 0
            pos = 0
            neu = 0
            for t in twitter_data:
                neg += t["neg"]
                pos += t["pos"]
                neu += t["neu"]
            
            print(neg)
            print(pos)
            print(neu)


def main():
    events = read_events()
    stock_sent_day_normalized(events)


if __name__ == "__main__":
    main()
