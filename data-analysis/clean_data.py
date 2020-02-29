import pycountry
import json
import re

# // - Same tweets from the same user
# // - location = null
# // - discard neutral after sentiment analysis - try without removing them
# // - check if a person tweets more than 3 times in a certain time period. He shouldn't tweet every 10 seconds for example because that's a bot

# read events.json 
def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


def search_location(location):
    country = None
    for location_part in location:
        try:
            country = pycountry.countries.search_fuzzy(location_part)
            break
        except:
            try:
                country = pycountry.countries.lookup(location_part)
                break
            except:
                continue
    return country


def suppress_data(events):
    for event in events["events"]:
        event_file = event["start_date"] + "_" + event["end_date"] + ".json"
        with open("tweets/" + event_file, 'r') as read_file:
            # list (array) of tweets
            full_tweets = json.load(read_file)["tweets"]
            # iterrate the tweets for each event
            tweets = { "tweets": [] }
            count_undiscovered = 0
            for t in full_tweets:
                if t["user"]["location"] != None:
                    country = None
                    # loc = t["user"]["location"].split(',')
                    location = re.split('; |- |,', t["user"]["location"])
                    found = False
                    for location_part in location:
                        try:
                            country = pycountry.countries.search_fuzzy(location_part)
                            found = True
                            break
                        except:
                            try:
                                country = pycountry.countries.lookup(location_part)
                                found = True
                                break
                            except:
                                continue

                    if not found:
                        location = t["user"]["location"].split(' ')
                        country = search_location(location)
                        if not country:
                            print(t["user"]["location"])
                            count_undiscovered += 1
                    if country:
                        tweet = {
                            "created_at": t["created_at"],
                            "user_id": t["user"]["id"],
                            "user_location": {
                                'alpha_2': country.alpha_2,
                                'alpha_3': country.alpha_3,
                                'name': country.name,
                                'numeric': country.numeric,
                                'official_name': country.official_name
                            },
                            "user_followers": t["user"]["followers_count"]
                        }

                        if "retweeted_status" in t:
                            try:
                                tweet["text"] = t["retweeted_status"]["extended_tweet"]["full_text"]
                            except:
                                tweet["text"] = t["retweeted_status"]["text"]
                        else:
                            try:
                                tweet["text"] = t["extended_tweet"]["full_text"]
                            except:
                                tweet["text"] = t["text"]

                        tweets["tweets"].append(tweet)
                        print(count_undiscovered)

        # TODO: Remove comments to store cleaned data in another directory
        # later we will perform sentiment analysis
        # store the cleaned data
        if len(tweets["tweets"]) > 0:
            with open("tweets/cleaned/" + event_file, 'w') as outfile:
                json.dump(tweets, outfile, ensure_ascii=True, indent=4)


def main():
    events = read_events()
    suppress_data(events)


if __name__ == "__main__":
    main()
