from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import json
import sys
import os


def sentiment_analysis():
    with open("events.json", "r") as events_file:
        events = json.load(events_file)

        # perform sentiment analysis for each event
        for event in events["events"]:
            filename = event["start_date"] + "_" + event["end_date"] + ".json"
            with open("tweets/cleaned/" + filename, "r") as twitter_file:
                twitter_data = json.load(twitter_file)        

                analyzer = SentimentIntensityAnalyzer()
                for i in range(0, len(twitter_data["tweets"])):
                    td = twitter_data["tweets"][i]
                    vs = analyzer.polarity_scores(td["text"])
                    td["neg"] = vs["neg"]
                    td["neu"] = vs["neu"]
                    td["pos"] = vs["pos"]
                    td["compound"] = vs["compound"]
                
                # here we have the results of sentiment analysis for this event - write to file
                with open("results_sa/" + filename, 'w') as outfile:
                    json.dump(twitter_data, outfile, ensure_ascii=True, indent=4)


def main():
    sentiment_analysis()


if __name__ == "__main__":
    main()
