import pycountry
import json

# // - Same tweets from the same user
# // - location = null
# // - discard neutral after sentiment analysis - try without removing them
# // - check if a person tweets more than 3 times in a certain time period. He shouldn't tweet every 10 seconds for example because that's a bot

# read events.json 
def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


def suppress_data(events):
    for event in events["events"]:
        event_file = event["start_date"] + "_" + event["end_date"] + ".json"
        with open("tweets/" + event_file, 'r') as read_file:
            # list (array) of tweets
            full_tweets = json.load(read_file)["tweets"]
            
            mapping = {country.name: country.alpha_2 for country in pycountry.countries}
            # iterrate the tweets for each event
            tweets = { "tweets": [] }
            for t in full_tweets:    
                
                if t["user"]["location"] != None:
                    try:
                        location = [t["user"]["location"]]
                        standard_name = cc.convert(names = location, to = 'name_short')
                        print(standard_name, " - ", t["user"]["location"])
                    except:
                        print("None - ", t["user"]["location"])
                    
                # if t["user"]["location"] not None:
                #     tweet = {}
                #     tweet["created_at"] = t["created_at"]
                #     tweet["user_id"] = t["user"]["id"]
                #     tweet["user_location"]= t["user"]["location"]
                #     tweet["user_followers"] = t["user"]["followers_count"]



                #     if "extended_tweet" in t:
                #         try:
                #             tweet = t["extended_tweet"]["full_text"]
                #         except:
                #             tweet = t["text"]
                #     elif "retweeted_status" in t:
                #         try:
                #             tweet = t["retweeted_status"]["extended_tweet"]["full_text"]
                #         except:
                #             tweet = t["retweeted_status"]["text"]
                #     else:
                #         tweet = t["text"]

                #     tweets["tweets"].append(tweet)
                #     # if "retweeted_status" in t:
                #     #     try:
                #     #         tweet = t["retweeted_status"]["extended_tweet"]["full_text"]
                #     #     except:
                #     #         tweet = t["retweeted_status"]["text"]
                #     # else:
                #     #     try:
                #     #         tweet = t["extended_tweet"]["full_text"]
                #     #     except:
                #     #         tweet = t["text"]

                
        break


        # TODO: Remove comments to store cleaned data in another directory
        # later we will perform sentiment analysis
        # store the cleaned data
        # if len(tweets["tweets"]) > 0:
        #     with open("tweets/cleaned/" + event_file, 'w') as outfile:
        #         json.dump(tweets, outfile, ensure_ascii=True, indent=4)


def main():
    events = read_events()
    suppress_data(events)


if __name__ == "__main__":
    main()
