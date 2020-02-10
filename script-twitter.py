import tweepy
import json
import sys



def main(argv):
    CONSUMER_KEY = '6yNXUwcoyPfMoVViacpdrF7X5'
    CONSUMER_SECRET = 'QGI3UIp95m7q7RVzoUMjf7pNDllteakjCVFFiLRAefLLs1CsAh'

    ACCESS_TOKEN = '104279299-9GYsUfGcTZcafEJM1dFYthWOjj4rxHfE9EnX1OvV'
    ACCESS_TOKEN_SECRET = 'wjPxY51tcZZgE1JhhJu4bw7E7fRjm75IlLm9oQmZPxAWF'


    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                time.sleep(15 * 60)


    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    query = ''
    for i in argv[2:]:
        query += i
        query += ' '

    # results = api.search(q="#cybertruck #teslacybertruck", since='19-10-2019', until='24-10-2019', lang='en')
    results = []
    for items in limit_handled(tweepy.Cursor(api.search, q=query, since=argv[0], until=argv[1], lang="en").items(100)):
        results.append(items)

    results_json = json.dumps(results)


    with open('data.txt', 'w') as outfile:
        json.dump(results_json, outfile)




if __name__ == "__main__":
    main(sys.argv[1:])
