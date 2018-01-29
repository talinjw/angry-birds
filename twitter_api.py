import re
import tweepy
import sys
from tweepy import OAuthHandler
from textblob import TextBlob
from pprint import pprint

DEBUG = True
 
class TwitterClient(object):
    ''' Generic Twitter Class for sentiment analysis '''

    
    def __init__(self):
        # Class constructor (initialization)

        CONSUMER_KEY = "w9HkzU3sXDkyGjfhe8awqe1mH"
        CONSUMER_SECRET = "BM59WwD1TfCgDp0upeCcCTj53dui31OGx9y8Z3kLJfGNPMPRfa"
        
        ACCESS_TOKEN = "930302623235764224-xC6DOUcngDZAJP4vLk6GKoL5Bua6Jbw"
        ACCESS_TOKEN_SECRET = "EGxrlKiyPAgC1FTdpjtzGyiIwl3xlB5WlaNKTY9hj72HT"
 
        try:
            # Try oAuth; pass access token + secret; if success, create tweepy object
            self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            self.api = tweepy.API(self.auth)
            
        except:
            print("Error: Authentication Failed")

 
    def clean(self, tweet):
        # Remove links + special chars
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

 
    def get_sentiment(self, tweet):
        # Classify tweet sentiment using textblob.sentiment()
    
        analysis = TextBlob(self.clean(tweet))
        if analysis.sentiment.polarity > 0:
            return "positive"
                               
        elif analysis.sentiment.polarity == 0:
            return "neutral"
                               
        else:
            return "negative"

 
    def get_tweets(self, query):
        # Fetch tweets via twitter API
        # https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets

        tweets = []
        
        try:
            fetched_tweets = self.api.search(q = query, lang = "en", count = 100)

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet["text"] = tweet.text.encode("UTF-8", errors="ignore")
                parsed_tweet["sentiment"] = self.get_sentiment(tweet.text)
 
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                               
                else:
                    tweets.append(parsed_tweet)

            return tweets
 
        except tweepy.TweepError as e:
            print("Error : {}".format(str(e)))


def get_analysis(query):
    # Return a specified number of tweets related to a given query

    api = TwitterClient()
    tweets = api.get_tweets(query = query)
    return tweets


if __name__ == "__main__":
                               
    QUERY = "Talin"
    print(("Query: '{}'").format(QUERY))

    tweets = get_analysis(QUERY)
    positive_tweets = [tweet for tweet in tweets if tweet["sentiment"] == "positive"]    
    negative_tweets = [tweet for tweet in tweets if tweet["sentiment"] == "negative"]

    total_tweets = len(tweets)
    print(("Total tweets returned: {}\n\n").format(total_tweets))
    
    p_count = len(positive_tweets)
    n_count = len(negative_tweets)
    
    print("Positive: {} %".format(100*p_count/total_tweets))
    print("Negative: {} %".format(100*n_count/total_tweets))
    print("Neutral: {} %".format(100*(total_tweets - p_count - n_count)/total_tweets))

    # positive tweets
    print("\n\nPositive tweets:")
    for tweet in positive_tweets[:50]:
        print(tweet["text"])
 
    # negative tweets
    print("\n\nNegative tweets:")
    for tweet in negative_tweets[:50]:
        print(tweet["text"])

    # all tweets
    print("\n\All tweets:")
    for tweet in tweets:
        print(tweet["text"])
