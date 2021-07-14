# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:36:14 2020

@author: Admin
"""

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 



API_KEY = 'ypZXMeDObRtxuXQfgVxwkSsVy'
API_SECRET = "9hIAdnEowR5SdlQdjxqzJNq2cBxAcyL0miaTLjqR2WBpdboSCH"
ACCESS_TOKEN = "781729372852092928-C0uAcqB4DamMbB01YHd78qcXGGZyw4Z"
ACCESS_TOKEN_SECRET =  "5rZfpCm7URjqcExspRz2CdXYiLMgya6NE5yyl0WLmhGQt"
    
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

data = tweepy.Cursor(api.search, q="Kunalkarma").items(2000)



tweets = []    
 
for tweet in data:
    try:
        parsed_tweet = {} 

	 #try:			# saving text of tweet 
        parsed_tweet['text'] = tweet.text
    
        clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())            
                
        analysis = TextBlob(clean_tweet) 
    
        if analysis.sentiment.polarity > 0:
            parsed_tweet['sentiment'] ='positive'
            print 'positive'
        elif analysis.sentiment.polarity == 0:
            parsed_tweet['sentiment'] ='neutral'
            print 'neutral'
        else:
            parsed_tweet['sentiment'] ='negative'
            print 'negative'
    
        if tweet.retweet_count > 0:
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
             tweets.append(parsed_tweet) 
    except:
        pass
         
         
         
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    
print 'total number of tweets %s' % len(tweets)
# percentage of positive tweets 
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
# percentage of negative tweets 
print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
# percentage of neutral tweets 
    
p_n_tweets = len(ntweets) + len(ptweets)
print("Neutral tweets percentage: {} %".format(100*(len(tweets)-p_n_tweets)/len(tweets))) 