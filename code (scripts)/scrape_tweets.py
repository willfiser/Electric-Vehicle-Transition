import time
import tweepy
import configparser
import pandas as pd

# function for pulling tweets from Twitter API
# Flow of the function goes like this:
# * Loop through all of the keywords
#   * For each of the keywords pull down 250 tweets
#   * Add tweets to appropriate arrays
#   * Exclude the words that we already searched for when the function eventually times out (because of the API limitation)
# * Return keywords
def _pull_tweets(api, keywords, tweets_all, processed_keywords): 
    if len(keywords) > 0:
        try: 
            for idx, keyword in enumerate(keywords):
                print(f'working on {keyword}')
                # pull down tweets
                tweets = tweepy.Cursor(api.search_tweets, q=keyword + " -filter:retweets", lang="en", tweet_mode='extended').items(250)

                # Collect a list of tweets
                tweets_all.extend({'created_at': tweet.created_at, 'text': tweet.full_text, 'keyword': keyword} for tweet in tweets)
                processed_keywords.append(keyword)
        except:
            print(f'last keyword that is processed {processed_keywords[-1]}')
            last_index = keywords.index(processed_keywords[-1])
            keywords = keywords[last_index+1:]

        return keywords, tweets_all, processed_keywords
    else:
        return None, None, None

# setup api keys and secrets that we'll use to authenticate
config = configparser.ConfigParser()
config.read('code (scripts)/tweet_config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# perform authentication 
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# keywords that we'll use to search the twitter API
keywords = ['love AND tesla', 'rivian', 'lucid AND air AND car', 'electric AND vehicle', 'hate AND electric AND car']

tweets_all = []
processed_keywords = []

# get first round of tweets
keywords, tweets_all, processed_keywords = _pull_tweets(api, keywords, tweets_all, processed_keywords)

# save results to a flat file
final_df = pd.DataFrame(tweets_all)
final_df.to_csv("ev_tweets_raw.csv")