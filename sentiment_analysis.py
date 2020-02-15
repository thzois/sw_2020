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
            with open("tweets/" + filename, "r") as twitter_file:
                twitter_data = json.load(twitter_file)        
                # create a list of the tweets
                tweets = []
                for tweet in twitter_data["tweets"]:
                    tweets.append(tweet["retweeted_status"]["extended_tweet"]["full_text"])
                
                # sentiment analysis 
                analyzer = SentimentIntensityAnalyzer()
                results = { "sent_analysis": [] }
                for t in tweets:
                    vs = analyzer.polarity_scores(t)
                    vs["tweet"] = t
                    results["sent_analysis"].append(vs)
                
                # here we have the results of sentiment analysis for this event - write to file
                with open("results_sa/" + filename, 'w') as outfile:
                    json.dump(results, outfile, ensure_ascii=True, indent=4)


def main():
    sentiment_analysis()


if __name__ == "__main__":
    main()
