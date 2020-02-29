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
                                'official_name': country[0].official_name if hasattr(country[0],'official_name') else None
                            },
                            "user_followers": t["user"]["followers_count"],
                            'is_duplicate': False
                        }
                    ### testing start
                    # tweet = {
                    #     "created_at": datetime.strptime(t["created_at"], "%a %b %y %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S"),
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
                tweets_per_user.get(tweet['user_id'])['tweets'].append(tweet)
        print(tweets_per_user)

        # Sort by date
        for user_id, user_data in tweets_per_user.items():
            user_data['tweets'].sort(key=lambda x: datetime.strptime(x['created_at'], "%Y-%m-%d %H:%M:%S"))

        # # Identify bots
        for user_id, user_data in tweets_per_user.items():
                tweet_date = None
                times_found_in_30_sec = 0
                for tweet in user_data['tweets']:
                    if tweet_date:
                        if (datetime.strptime(tweet['created_at'], "%Y-%m-%d %H:%M:%S") - tweet_date).seconds < 10:
                            times_found_in_30_sec += 1
                        else:
                            times_found_in_30_sec = 0

                    tweet_date = datetime.strptime(tweet['created_at'], "%Y-%m-%d %H:%M:%S")

                    if times_found_in_30_sec == 3:
                        user_data['is_bot'] = True
                        print("BOT FOUND")

        # # remove bots
        tweets_per_user_no_bots = {}
        for user_id, user_data in tweets_per_user.items():
            if user_data['is_bot']:
                continue
            tweets_per_user_no_bots.update({user_id: user_data})

        # # identify duplicate tweets per user
        for user_id, user_tweets in tweets_per_user_no_bots.items():
            for i in range(0, len(user_tweets['tweets']) - 1):
                for j in range(i + 1, len(user_tweets['tweets'])):
                    if user_tweets['tweets'][i]['text'] == user_tweets['tweets'][j]['text']:
                        user_tweets['tweets'][i]['is_duplicate'] = True

        tweets_per_user_final = {}
        for user_id, user_data in tweets_per_user_no_bots.items():
            for tweet in user_data['tweets']:
                if tweet['is_duplicate']:
                    continue
                if tweets_per_user_final.get(user_id):
                    tweets_per_user_final[user_id]['tweets'].append(tweet)
                else:
                    tweets_per_user_final.update({user_id: {'tweets': [tweet]}})

        if len(tweets_per_user_final["tweets"]) > 0:
            with open("tweets/cleaned/" + event_file, 'w') as outfile:
                json.dump(tweets_per_user_final, outfile, ensure_ascii=True, indent=4)


def main():
    events = read_events()
    clean_data(events)


if __name__ == "__main__":
    main()
