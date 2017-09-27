import tweepy
import time
import json
import re
from pprint import pprint
import string
import unidecode
from urllib.parse import quote_plus

def authenticate():
    #consumer key, secret, app key, secret
    keys = ['6MtEg33yEnTMw2rNGyOZMSYi4',
    'pmLWbRqXYVTUVsi6GngMsIwmIzceUj273LCYJ8Fcu1KPNcTFvi',
    '321020505-UqnEWtPZDunXeGUbJADLt89y9FUS4xXQFGcd8hpE',
    'vNG1slpiQs8zgHwe8ImkdkpCuUrS2pDUPHStBOYWAx0EZ']
    
    #OAuth process
    auth = tweepy.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])
    
    #the interface
    global api
    api = tweepy.API(auth)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15*60)

def timelineCrawl(n):
    return [tweet for tweet in limit_handled(tweepy.Cursor(api.home_timeline).items(n))]

def search(query, n):
    cleanQuery = quote_plus(query)
    searched_tweets = []
    tweet_ids = set()
    rType = "mixed"
    last_id = -1
    while len(searched_tweets) < n:
        try:
            if last_id != -1:
                new_tweets = api.search(q=cleanQuery, lang = "es", result_type=rType, max_id=last_id - 1, tweet_mode = "extended")
            else:
                new_tweets = api.search(q=cleanQuery, lang = "es", result_type=rType, tweet_mode = "extended")
            
            if not new_tweets:  break

            for tweet in new_tweets:
                if tweet.id not in tweet_ids and tweet.full_text[:2] != "RT":
                    tweet_ids.add(tweet.id)
                    searched_tweets.append(tweet)

            # print(len(searched_tweets))
            last_id = min(tweet_ids)

        except tweepy.RateLimitError as e:
            print("Waiting 15 minutes...")
            time.sleep(15 * 60)
            print("Done waiting")
            break
        except tweepy.TweepError as e:
            print("Did NOT exceed rate limit: ", e)
            break



    return searched_tweets

def tweetCleanse(tw):
    tweet = tw._json

    #extract emojis
    emojip = re.compile("(" +"|".join(ours) + ")")
    matches = emojip.findall(tweet["full_text"])

    urlp = re.compile("\s*http\S*")
    spacep = re.compile("\s+", re.MULTILINE)
    punctp = re.compile("[{}]".format(string.punctuation+","))
    
    # delete mentions
    for mention in reversed(tweet["entities"]["user_mentions"]):
        tweet["full_text"] = tweet["full_text"][: mention["indices"][0] ] + tweet["full_text"][mention["indices"][1] :]

    # hashtags have no #
    tweet["full_text"] = tweet["full_text"].replace("#", "")

    # no urls
    tweet["full_text"] = urlp.sub('', tweet["full_text"])

    # no punctuation
    tweet["full_text"] = punctp.sub('', tweet["full_text"])

    #lower case
    tweet["full_text"] = tweet["full_text"].lower()

    #no extra spaces
    tweet["full_text"] = spacep.sub(' ', tweet["full_text"])

    # no accents
    tweet["full_text"] = unidecode.unidecode(tweet["full_text"])

    toRet = {k:tweet[k] for k in tweet.keys() & ( "id", "full_text")} 
    toRet["emojis"] = matches
    return toRet

def searchWithEmoji(query, n):
    toRet = []
    sliceSize = n//8
    global ours
    ours = ["😂","❤️","😍","♥️","😭","😊","😒","💕","😘","😩","👌","😔","😏","😁","😉","👍","😌","🙏","🎶","😢","😅","😎","👀","😳","🙌","💔","🙈","✌️","💙","✨","💜","💯","😴","💖","😄","😑","😕","😜","😞","😋","😪","😐","👏","🔥","💗","💘","💁","💞","👉","📷","💋","🙊","😱","✋","😈","😡","🎉","😃","💀","💛","💪","😫","😝","😆","👊","😀","🌚","😤","☀️","💓","💚","😓","😻","✔️","😣","👈","😷","😇","😛","😚","😥","👋","👑","😬","😖","😠","🌟","🎵","😶","👇","🙋","👎","💃","🔴","🔫","💫","👅","💥","💭","✊","✈️","💩","😰","😹","🙅","🌞","💦","💎","🙆","⚡️","⭐️","💤","🍕","👻","🍀","⚽️","🎤","😟","😨","🚶","🔞","🎀","😙","👽","💅","☝️","🌙","🙇","☁️","🍻","😧","💟","👯","👼","☕️","💝","🎁","🐶","💰","☎️","🎂","😮","🏃","😵","😲","✖️","😯","🐱","👆","👫","🏆","🌝","💸","💍","😿"]
    
    for i in range(8):
        toRet += search(query + " ("+  " OR ".join(ours[ 20*i : min( 20*(i+1), 20*i + ( len(ours) - 20*i ) ) ]) + " )", sliceSize)

    return toRet


def main():
    authenticate()
    query = "iphone"
    number = 30

    print( json.dumps({ "tweets" : [ tweetCleanse(tweet) for tweet in searchWithEmoji(query, number) ] }))


main()