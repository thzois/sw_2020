from datetime import datetime
import pycountry
import json
import re


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


def clean_data(events):
    for event in events["events"]:
        event_file = event["start_date"] + "_" + event["end_date"] + ".json"
        with open("tweets/" + event_file, 'r') as read_file:
            # list (array) of tweets
            full_tweets = json.load(read_file)["tweets"]
            # iterrate the tweets for each event
            tweets = { "tweets": [] }

            # statistics
            total_tweets = len(full_tweets)
            total_tweets_loc = 0
            total_tweets_loc_undesc = 0
            
            for t in full_tweets:
                if t["user"]["location"] != None:
                    total_tweets_loc += 1
                    location = re.split('; |- |,', t["user"]["location"])
                    country = search_location(location)

                    if not country:
                        location = t["user"]["location"].split(' ')
                        country = search_location(location)
                        if not country:
                            total_tweets_loc_undesc += 1
                    if country:
                        tweet = {
                            "created_at": datetime.strptime(t["created_at"], "%a %b %y %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S"),
                            "user_id": t["user"]["id"],
                            "user_location": {
                                'alpha_2': country[0].alpha_2,
                                'alpha_3': country[0].alpha_3,
                                'name': country[0].name,
                                'numeric': country[0].numeric,
                                'official_name': country[0].official_name
                                if hasattr(country[0], 'official_name') else None
                            },
                            "user_followers": t["user"]["followers_count"],
                            'is_duplicate': False
                        }
                    ### testing start
                    # tweet = {
                    #     "created_at": datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S"),
                    #     "user_id": t["user"]["id"],
                    #     "user_followers": t["user"]["followers_count"],
                    #     'is_duplicate': False
                    # }
                    ### testing end

                        if "extended_tweet" in t:
                            try:
                                tweet["text"] = t["extended_tweet"]["full_text"]
                            except:
                                tweet["text"] = t["text"]
                        elif "retweeted_status" in t:
                            try:
                                tweet["text"] = t["retweeted_status"]["extended_tweet"]["full_text"]
                            except:
                                tweet["text"] = t["retweeted_status"]["text"]
                        else:
                            tweet["text"] = t["text"]

                        tweets["tweets"].append(tweet)

        tweets_per_user = {}
        for tweet in tweets['tweets']:
            user_tweets = tweets_per_user.get(tweet['user_id'])
            if not user_tweets:
                tweets_per_user.update({tweet['user_id']: {
                    'tweets': [tweet],
                    'is_bot': False
                    }})
            else:
                print(user_tweets)
                user_tweets['tweets'].append(tweet)
        print(tweets_per_user)

        # Sort by date
        for user_id, user_data in tweets_per_user.items():
            user_data['tweets'].sort(key=lambda x: datetime.strptime(x['created_at'], "%Y-%m-%d %H:%M:%S"))

        tweets_per_user_final = {}
        # identify duplicate tweets per user
        for user_id, user_tweets in tweets_per_user.items():
            tweets_per_user_final.update({user_id: [user_tweets['tweets'][0]]})
            for i in range(1, len(user_tweets['tweets'])):
                found_duplicate = False
                for tweet in tweets_per_user_final[user_id]:
                    if user_tweets['tweets'][i]['text'] == tweet['text']:
                        found_duplicate = True
                        print("duplication removed")
                if not found_duplicate:
                    tweets_per_user_final[user_id].append(user_tweets['tweets'][i])

        if len(tweets_per_user_final) > 0:
            with open("tweets/cleaned/" + event_file, 'w+') as outfile:
                json.dump(tweets_per_user_final, outfile, ensure_ascii=True, indent=4)


def main():
    events = read_events()
    clean_data(events)


if __name__ == "__main__":
    main()
