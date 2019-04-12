import re 
import tweepy
import csv
import datetime
from tweepy import OAuthHandler 
from textblob import TextBlob 
class Test:
    def __init__(self,query="",count=0,list1=[''],list2=[''],positive=0,negative=0,neutral=0):
        self.query =query
        self.count = count
        self.list1=list1
        self.list2=list2
        self.positive=positive
        self.negative=negative
        self.neutral=neutral

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


	def get_tweets(self, query, count):
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
def csvout2(Test):
	file_name = "archive/Sentiment_Analysis_of__Tweets_About_{}_at_{}.csv".format(Test.query,datetime.datetime.now().date())

	with open(file_name, 'w', newline='') as csvfile:
   		csv_writer = csv.DictWriter(
       	f=csvfile,
       	fieldnames=["Tweet", "Sentiment"]
  		 )
   		csv_writer.writeheader()
   		for tweet in Test.list1:
   			csv_writer.writerow({
           		'Tweet': tweet,
           		'Sentiment': 'positive'
       })
def main(query,count): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets
	
	tweets = api.get_tweets(query, count)




	list1=[]



	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

	# percentage of positive tweets
	pptweets=round(100*len(ptweets)/len(tweets),2)
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

	# percentage of negative tweets
	list2=[]
	pntweets = round(100 * len(ntweets) / len(tweets), 2)


	# percentage of neutral tweets

	netweets=[x for x in tweets if x not in ptweets]
	netweets=[x for x in netweets if x not in ntweets]
	pnetweets = round(100 * len(netweets) / len(tweets), 2)



	# printing first 5 positive tweets
	for tweet in ptweets:
		list1.append(tweet['text'])

	# printing first 5 negative tweets


	for tweet in ntweets:
		list2.append(tweet['text'])





	return Test(query,count,list1,list2,pptweets,pntweets,pnetweets)


if __name__ == "__main__": 
	# calling main function 
	main(query,count)

