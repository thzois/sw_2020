from collections import OrderedDict
from operator import itemgetter

import pandas as pd
from datetime import datetime
from datetime import timedelta
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

        app_data = {}
        app_data["positive_percentage"] = 0
        app_data["negative_percentage"] = 0
        app_data["neutral_percentage"] = 0
        app_data["per_day"] = []

        total_neutral = 0
        total_positive = 0
        total_negative = 0

        # caclulate positivity per day
        with open("tweets/results/" + filename + ".json", "r") as twitter_file:
            twitter_data = json.load(twitter_file)["tweets"]

            start_dateobj = datetime.strptime(event["start_date"], '%Y-%m-%d').date()
            end_dateobj = datetime.strptime(event["end_date"], '%Y-%m-%d').date()            
            stock_index = 0
            aggr_data = True

            # calculate positivity per day
            while True:
                day_neu = 0
                day_pos = 0
                day_neg = 0
                
                for t in twitter_data:
                    t_date = datetime.strptime(t["created_at"].split(" ")[0], '%Y-%m-%d').date()
                    if (t["pos"] > t["neu"]) and (t["pos"] > t["neg"]):
                        if aggr_data: total_positive += 1
                        if t_date == start_dateobj: day_pos += 1

                    elif (t["neu"] > t["pos"]) and (t["neu"] > t["neg"]):
                        if aggr_data: total_neutral += 1
                        if t_date == start_dateobj: day_neu += 1

                    elif t["neu"] == t["pos"]:
                        if aggr_data: total_neutral += 1
                        if t_date == start_dateobj: day_neu += 1
                    else:
                        if aggr_data: total_negative += 1
                        if t_date == start_dateobj: day_neg += 1
                

                # convert to percentages - per day
                total_day = day_neg + day_neu + day_pos
                day_pos_perc = day_pos / total_day
                day_neg_perc = day_neg / total_day
                day_neu_perc = day_neu / total_day

                # apply positivity formula for that day 
                positivity = (day_pos_perc * 1.0) + (day_neu_perc * 0.5) + (day_neg_perc * 0)
                
                # get normalized and real Adj Close for that day
                stock_price_real = stock_df.iloc[stock_index]["Adj Close"]
                stock_price = stock_price_real / stock_df.iloc[idx_max]["Adj Close"]

                # store the data
                app_data["per_day"].append({ "date": start_dateobj.strftime("%Y-%m-%d"), "positivity": positivity, "stock_norm": stock_price, "stock_real": stock_price_real })
                
                # if the day is the next day of our end_date break
                start_dateobj = start_dateobj + timedelta(days=1)
                stock_index += 1
                aggr_data = False
                if start_dateobj > end_dateobj:
                    break

            pos_perc = (100*total_positive) / len(twitter_data)
            neg_perc = (100*total_negative) / len(twitter_data)
            neu_perc = (100*total_neutral) / len(twitter_data)

            app_data["positive_percentage"] = pos_perc
            app_data["negative_percentage"] = neg_perc
            app_data["neutral_percentage"] = neu_perc

            with open(f"../web-app/results/sentiment/{filename}.json", 'w') as outfile:
                json.dump(app_data, outfile, ensure_ascii=True, indent=4)



def prepare_barchart_data(events):
    for event in events["events"]:
        filename = event["start_date"] + "_" + event["end_date"]
        with open(f"tweets/results/{filename}.json", "r") as twitter_file:
            twitter_data = json.load(twitter_file)["tweets"]
            tweets_per_country = {}
            for t in twitter_data:
                country_name = t['user_location']['name']
                if tweets_per_country.get(country_name):
                    tweets_per_country[country_name] += 1
                else:
                    tweets_per_country.update(
                        {
                            country_name: 1
                        })
            sorted_tweets_per_country = OrderedDict(
                sorted(tweets_per_country.items(), key=itemgetter(1), reverse=True))

            with open(f"tweets/results/barcharts/{filename}.json", 'w') as outfile:
                json.dump(sorted_tweets_per_country, outfile, ensure_ascii=True, indent=4)



def main():
    events = read_events()
    stock_sent_day_normalized(events)
    prepare_barchart_data(events)



if __name__ == "__main__":
    main()
