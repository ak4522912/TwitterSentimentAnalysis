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
		consumer_key = 'Yb4MjUhlfaNH9An33iB8bAMnD'
		consumer_secret = 'Lbo4SzscCpYTb48OM5WcE1YLs0SsSUvEKXu3qeQJL1PTv1XaUq'
		access_token = '1103368213927215111-fgkLHPZ8DxQPyFHckZzlhBUbJgR2oD'
		access_token_secret = 'IpuGfIIj9SPkdf1VL7vLgHcFCcqQqmkcioA9F23WOC95p'

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

	def get_tweets(self, query, count = 10): 
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

def main(query): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
	tweets = api.get_tweets(query, count = 50)
	list1=['']

	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 

	# percentage of positive tweets 
	str1=("Positive tweets percentage: {} %".format(round(100*len(ptweets)/len(tweets),2)))
	list1.append(str1)
	# picking negative tweets from tweets 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	# percentage of negative tweets 
	str1=("Negative tweets percentage: {} %".format(round(100*len(ntweets)/len(tweets),2)))
	list1.append(str1)
	# percentage of neutral tweets
	pntweets=[x for x in tweets if x not in ptweets]
	pntweets=[x for x in pntweets if x not in ntweets]

	str1=("Neutral tweets percentage: {}%".format(round(100*len(pntweets)/len(tweets),2)))
	list1.append(str1)

	# printing first 5 positive tweets 
	str1=("\n\nPositive tweets:")
	list1.append(str1)
	for tweet in ptweets[:20]:
		list1.append(tweet['text'])

	# printing first 5 negative tweets 
	str1=("\n\nNegative tweets:")
	list1.append(str1)
	for tweet in ntweets[:20]:
		list1.append(tweet['text'])
	return list1
if __name__ == "__main__": 
	# calling main function 
	main(query)
