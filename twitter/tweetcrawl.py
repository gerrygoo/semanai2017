import tweepy
import time
import json
import re
import emoji
from urllib.parse import quote_plus

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15*60)

def search(query, n):
    cleanQuery = quote_plus(query)
    searched_tweets = []
    tweet_ids = set()
    tpp = 100 #tweets per page>
    rType = "mixed"
    last_id = -1
    emojiRegex = emoji.get_emoji_regexp()
    while len(searched_tweets) < n:
        try:
            if last_id != -1:
                new_tweets = api.search(q=cleanQuery, lang = "es", result_type=rType, count=tpp, max_id=last_id - 1, tweet_mode = "extended")
            else:
                new_tweets = api.search(q=cleanQuery, lang = "es", result_type=rType, count=tpp, tweet_mode = "extended")
            
            if not new_tweets:  break

            for tweet in new_tweets:
                if tweet.id not in tweet_ids and emojiRegex.search(tweet.full_text):
                    tweet_ids.add(tweet.id)
                    searched_tweets.append(tweet)
                    print(tweet.full_text)


            print(len(searched_tweets))
            last_id = min(tweet_ids)

        except tweepy.RateLimitError as e:
            print("Waiting 15 minutes...")
            sleep(15 * 60)
            print("Done waiting")
            break
        except tweepy.TweepError as e:
            print("Did NOT exceed rate limit: ", e)
            break

    return searched_tweets


def timelineCrawl(n):
    return [tweet for tweet in limit_handled(tweepy.Cursor(api.home_timeline).items(n))]


#consumer key, secret, app key, secret
keys = ['6MtEg33yEnTMw2rNGyOZMSYi4',
'pmLWbRqXYVTUVsi6GngMsIwmIzceUj273LCYJ8Fcu1KPNcTFvi',
'321020505-UqnEWtPZDunXeGUbJADLt89y9FUS4xXQFGcd8hpE',
'vNG1slpiQs8zgHwe8ImkdkpCuUrS2pDUPHStBOYWAx0EZ']
 
#OAuth process
auth = tweepy.OAuthHandler(keys[0], keys[1])
auth.set_access_token(keys[2], keys[3])
 
#the interface
api = tweepy.API(auth)


search("mackeeper", 10)
# for i in search("mackeeper", 10):
#     print(i.full_text)
