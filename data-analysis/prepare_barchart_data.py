import json
from collections import OrderedDict
from operator import itemgetter


def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


def prepare_barchart_data(events):
    for event in events["events"]:
        filename = event["start_date"] + "_" + event["end_date"]
        # stock_df.to_csv('../web-app/results/stocks/' + filename, index = False)
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

            sorted_tweets_per_country = OrderedDict(sorted(
                tweets_per_country.items(), key=itemgetter(1), reverse=True))

            with open(f"../web-app/results/barcharts/{filename}.json", 'w+') as outfile:
                json.dump(sorted_tweets_per_country, outfile, ensure_ascii=True, indent=4)


def main():
    events = read_events()
    prepare_barchart_data(events)


if __name__ == "__main__":
    main()
