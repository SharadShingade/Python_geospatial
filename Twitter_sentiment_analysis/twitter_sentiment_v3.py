# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:06:08 2020

@author: Admin
"""

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'ypZXMeDObRtxuXQfgVxwkSsVy'
		consumer_secret = "9hIAdnEowR5SdlQdjxqzJNq2cBxAcyL0miaTLjqR2WBpdboSCH"
		access_token = "781729372852092928-C0uAcqB4DamMbB01YHd78qcXGGZyw4Z"
		access_token_secret =  "5rZfpCm7URjqcExspRz2CdXYiLMgya6NE5yyl0WLmhGQt"


		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 200000): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    '''
    API_KEY = 'ypZXMeDObRtxuXQfgVxwkSsVy'
    API_SECRET = "9hIAdnEowR5SdlQdjxqzJNq2cBxAcyL0miaTLjqR2WBpdboSCH"
    ACCESS_TOKEN = "781729372852092928-C0uAcqB4DamMbB01YHd78qcXGGZyw4Z"
    ACCESS_TOKEN_SECRET =  "5rZfpCm7URjqcExspRz2CdXYiLMgya6NE5yyl0WLmhGQt"
    
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    '''
    # calling function to get tweets 
    
    tweets = api.get_tweets(query ='kunal kamra', count = 200000) 
    
    
    ## Trial 
    # Define the search term and the date_since date as variables
    '''
    search_words = "#article15"
    date_since = "2019-06-28"
    
    tweets = tweepy.Cursor(api.search,q=search_words,lang="en",since=date_since).items(2000)

    query = '#article15'
    max_tweets = 1000
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
    '''
  
    # picking positive tweets from tweets 
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
  
    # printing first 5 positive tweets 
    
    '''
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 
  
    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 
    '''
  
if __name__ == "__main__": 
    # calling main function 
   