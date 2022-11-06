import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 

def run_twitter_etl():

    access_key = "Zf5wwCnL7YDYcJOcJuGSFfgOC" 
    access_secret = "gSzjrVve022qbUjhrC9DKqhMkuPXWYved5bVoWIR5OiNkwPBof" 
    consumer_key = "1588675166225195008-DT5Tay1JYo6ApL5uovC4fuQUf39sSi"
    consumer_secret = "KCdhZomPMmRN1MJIoNWxAI5Baw1c9VppSs2JyiwVRHyG6"

    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # # # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )

    tweet_list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        tweet_list.append(refined_tweet)

    df = pd.DataFrame(tweet_list)
    #df.to_csv('redefined_tweets.csv')
    df.to_csv('s3://airflow-test-etl-pipeline/elonmusk_twitter_data.csv')