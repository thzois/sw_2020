from collections import OrderedDict
from operator import itemgetter

import pandas as pd
from datetime import datetime
from datetime import timedelta
import json
import glob
import csv
import sys
import os


def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


def remove_old_html_files():
    file_list = glob.glob('../web-app/event*.html') 
    for file_path in file_list:
        try:
            os.remove(file_path)
        except:
            print("Error while deleting file : ", file_path)


def generate_html(events):
    navbars = []
    statistics = []
    sentiment_vs_stock_charts = []
    sentiment_gauges = []
    world_maps = []
    files = []
    
    for i in range(1, len(events['events']) + 1):
        # navbar
        nav = ''
        # DO NOT MODIFY THE SPACING IN THE NAV STRING
        for j in range(1, len(events['events']) + 1):
            if i == j:
                # add style=color: white (active page)
                nav += f'\
         <li class="nav-item">\n \
            <a class="nav-link js-scroll-trigger" href="./event{j}.html" style="color: white">Event {j}</a>\n \
         </li>\n '
            else:
                nav += f'\
         <li class="nav-item">\n \
            <a class="nav-link js-scroll-trigger" href="./event{j}.html">Event {j}</a>\n \
         </li>\n '

        nav += f'\
         <li class="nav-item">\n \
            <a href="https://github.com/thzois/sw_2020" target="_blank"><img src="./images/github_white.png" width="110" alt="Fork me on GitHub"></a>\n \
         </li>\n '

        navbars.append(nav)
        files.append(open(f'../web-app/event{i}.html', 'w'))

        # statistics - open file for this event
        for event in events["events"]:
            filename = event["start_date"] + "_" + event["end_date"] + ".json"
            sentiment_vs_stock_charts.append("\t\t\t\t\t\tsentiment_vs_stock(ctx, '" + filename + "');\n")
            sentiment_gauges.append("\t\t\t\t\t\tsentiment_gauge(ctx, '" + filename + "');\n")
            world_maps.append(f"\t\t\t\t\t\tgenerate_world_map('{filename}');\n")

            with open("tweets/results/" + filename, "r") as twitter_file:
                twitterd = json.load(twitter_file)
                hashtags = ''
                for ht in event["hashtags"]:
                    # add 2 spaces
                    hashtags += ht + ' &nbsp;'

                # DO NOT MODIFY THE SPACING IN THE STATISTICS STRING
                statistics.append( 
    f'\
     <div class="row">\n \
        <div class="col-md-12 text-center">\n \
            <h3></br>{event["title"]}</h3>\n \
        </div>\n \
     </div>\n \
     <div class="row"><br></div>\n \
     <div class="row">\n \
         <div class="col-md-6">\n \
             <ul class="list-group">\n \
                 <li class="list-group-item active">Data collection information</li>\n \
                 <li class="list-group-item">Event start: <span class="highlight">{event["start_date"]}</span></li>\n \
                 <li class="list-group-item">Event end: &nbsp;<span class="highlight">{event["end_date"]}</span></li>\n \
                 <li class="list-group-item">Hashtags: <span class="highlight">{hashtags}</span></li>\n \
             </ul>\n \
         </div>\n \
         <div class="col-md-6">\n \
             <ul class="list-group">\n \
                 <li class="list-group-item active">Processing information</li>\n \
                 <li class="list-group-item">Total tweets: <span class="highlight">{twitterd["total_tweets"]}</span></li>\n \
                 <li class="list-group-item">Tweets with location: <span class="highlight">{twitterd["tweets_with_location"]}</span></li>\n \
                 <li class="list-group-item">Tweets with unknown location: <span class="highlight">{twitterd["tweets_disc_unknown_location"]}</span></li>\n \
                 <li class="list-group-item">Duplicate tweets: <span class="highlight">{twitterd["duplicate_tweets"]}</span></li>\n \
             </ul>\n \
         </div>\n \
     </div>\n \
     <div class="row"><br>\n \
         <div class="col-md-12 text-center"><br>\n \
             <h5>Tweets analyzed: <span class="highlight">{twitterd["tweets_stored"]}</span></h5>\n \
         </div>\n \
     </div>\n')


    with open('event_template.html') as event_template_file:
        for line in event_template_file:
            idx = 0
            for file in files:
                file.write(line)
                if '### SWAnalytics NAV' in line:
                    file.write(f'\t\t\t\t<ul class="navbar-nav ml-auto">\n {navbars[idx]} \t\t\t</ul>\n')
                if '### SWAnalytics STATISTICS' in line:
                    file.write(statistics[idx])
                if '### SWAnalytics SENTIMENT_STOCK' in line:
                    file.write(sentiment_vs_stock_charts[idx])
                if '### SWAnalytics SENTIMENT_GAUGE' in line:
                    file.write(sentiment_gauges[idx])
                if '### SWAnalytics WORLD_MAP' in line:
                    file.write(world_maps[idx])
                idx += 1


def sentiment_data(events):
    for event in events["events"]:
        filename = event["start_date"] + "_" + event["end_date"]

        # normalize stocks
        stock_df = pd.read_csv("stocks/" + filename + ".csv")
        idx_max = stock_df["Adj Close"].idxmax()

        app_data = {}
        app_data["positive_percentage"] = 0
        app_data["negative_percentage"] = 0
        app_data["neutral_percentage"] = 0
        app_data["correlation_index"] = 0
        app_data["per_day"] = []

        total_neutral = 0
        total_positive = 0
        total_negative = 0

        df_tmp = { "stock_norm": [], "positivity": [] }

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

                # correlation index
                df_tmp["stock_norm"].append(stock_price)
                df_tmp["positivity"].append(positivity)

                # if the day is the next day of our end_date break
                start_dateobj = start_dateobj + timedelta(days=1)
                stock_index += 1
                aggr_data = False
                if start_dateobj > end_dateobj:
                    break

            # calculate event correlation index
            df = pd.DataFrame(data = df_tmp)
            correlation_index = df["positivity"].corr(df["stock_norm"])

            pos_perc = (100*total_positive) / len(twitter_data)
            neg_perc = (100*total_negative) / len(twitter_data)
            neu_perc = (100*total_neutral) / len(twitter_data)

            app_data["positive_percentage"] = pos_perc
            app_data["negative_percentage"] = neg_perc
            app_data["neutral_percentage"] = neu_perc
            app_data["correlation_index"] = correlation_index

            with open(f"../web-app/results/sentiment/{filename}.json", 'w') as outfile:
                json.dump(app_data, outfile, ensure_ascii=True, indent=4)


def world_data(events):
    for event in events["events"]:
        filename = event["start_date"] + "_" + event["end_date"]
        with open(f"tweets/results/{filename}.json", "r") as twitter_file:
            twitter_data = json.load(twitter_file)["tweets"]
            tweets_per_country = {}
            for t in twitter_data:
                country_name = t['user_location']['name']
                if tweets_per_country.get(country_name):
                    tweets_per_country[country_name]['tweets_count'] += 1
                    tweets_per_country[country_name]['positive_tweets_count'] += 1 if (t['pos'] > t['neu'] and t['pos'] > t['neg']) else 0
                    tweets_per_country[country_name]['neutral_tweets_count'] += 1 if (t['neu'] >= t['pos'] and t['neu'] >= t['neg']) else 0
                    tweets_per_country[country_name]['negative_tweets_count'] += 1 if (t['neg'] > t['neu'] and t['neg'] > t['pos']) else 0
                else:
                    tweets_per_country.update(
                        {
                            country_name: {
                                'id': t['user_location']['alpha_2'],
                                'name': country_name,
                                'tweets_count': 1,
                                'positive_tweets_count': 1 if (t['pos'] > t['neu'] and t['pos'] > t['neg']) else 0,
                                'neutral_tweets_count': 1 if (t['neu'] >= t['pos'] and t['neu'] >= t['neg']) else 0,
                                'negative_tweets_count': 1 if (t['neg'] > t['neu'] and t['neg'] > t['pos']) else 0
                            }
                        }
                    )

            for country_name, country_vals in tweets_per_country.items():
                positive_percentage = 100 * country_vals['positive_tweets_count'] / country_vals['tweets_count']
                neutral_percentage = 100 * country_vals['neutral_tweets_count'] / country_vals['tweets_count']
                negative_percentage = 100 * country_vals['negative_tweets_count'] / country_vals['tweets_count']

                positivity = (positive_percentage * 1.0) + (neutral_percentage * 0.5) + (negative_percentage * 0)

                country_vals['positive_percentage'] = positive_percentage
                country_vals['neutral_percentage'] = neutral_percentage
                country_vals['negative_percentage'] = negative_percentage
                country_vals['positivity'] = positivity

            tweets_per_country_final = []
            for country, country_data in tweets_per_country.items():
                tweets_per_country_final.append(country_data)

            with open(f"../web-app/results/world/{filename}.json", 'w') as outfile:
                json.dump(tweets_per_country_final, outfile, ensure_ascii=True, indent=4)


def main():
    events = read_events()
    sentiment_data(events)
    world_data(events)
    remove_old_html_files()
    generate_html(events)


if __name__ == "__main__":
    main()
