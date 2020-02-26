import pandas as pd
import json



# read events.json 
def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


def clean_data(events):
    for event in events["events"]:
        event_file = event["start_date"] + "_" + event["end_date"] + ".json"
        with open("tweets/" + event_file, 'r') as read_file:
            # list (array) of tweets
            tweets = json.load(read_file)["tweets"]
            
            # here clean data for ONE specific event
            print("I am cleaning data for", event_file, "which has", len(tweets), "tweets")
            

        # TODO: Remove comments to store cleaned data in another directory
        # later we will perform sentiment analysis
        # store the cleaned data
        # if len(tweets["tweets"]) > 0:
        #     with open("tweets/cleaned/" + event_file, 'w') as outfile:
        #         json.dump(tweets, outfile, ensure_ascii=True, indent=4)


def main():
    # events = read_events()
    # clean_data(events)
    print("CLEAN DATA")


if __name__ == "__main__":
    main()
