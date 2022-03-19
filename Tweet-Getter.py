#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from time import sleep, time
import twitter
import warnings

TWEETS_PER_CALL = 200
MAXIMUM_TWEETS = 3200
NUM_ITER = int(MAXIMUM_TWEETS / TWEETS_PER_CALL)

def initializeAPI():
	# Fill with your values
	api = twitter.Api(consumer_key='',
		consumer_secret='',
		access_token_key='',
		access_token_secret='')

	print("API initialized.")
	return api

def obtain_tweets(api, user, gets_rts):
	sleep_time = 0
	
	# Obtains the average sleep time in order to avoid bad API use
	try:
		rate_limit = api.CheckRateLimit("/statuses/user_timeline")
		
		# Normally, we already know the rate limit lasts 15 minutes, but I guess it's better to get that value dynamically
		current_time = int(time())
		diff = rate_limit.reset - current_time

		sleep_time = float(diff) / rate_limit.limit
	except twitter.error.TwitterError as e:
		print("Twitter error:", str(e))
		exit(1)

	data = []
	maxId = None

	# In this loop you obtain up to 200 tweets in each iteration
	# It is not endless because Twitter does not allow to get nothing after the 3200 newest tweets per user
	for i in range(NUM_ITER): 
		# The important call to retrieve data. We can avoid RTs or not
		statuses = None
		try:
			statuses = api.GetUserTimeline(screen_name=user,max_id=maxId,count=TWEETS_PER_CALL,include_rts=gets_rts)
		except twitter.error.TwitterError as e:
			print("Twitter error:", str(e))
			exit(1)

		# Ends if there aren't any tweets left before finishing the loop
		if len(statuses) == 0:
			print("Obtained tweets from", user + ".")
			return data

		# We are only interested in collecting the body text from the tweets
		data.extend([s.text for s in statuses])

		# Extracts ID from the last obtained tweet so we can filter correctly in next iteration
		# We subtract 1 to it to avoid this last tweet being repeated in the next chunk
		maxId = statuses[-1].id - 1

		# Sleep to obey the rate limits
		sleep(sleep_time)

	print("Obtained tweets from", user + ".")
	return data

def write_data_to_file(data, filename):
	try:
		file = open(filename, 'w')
		file.write("\n".join(data))
		print("Tweets written in", filename)
	except IOError:
		print("Error writing data to", filename)
		return

def main():
	# Customs behavior with console parameters
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", help = "Username", required = True)
	parser.add_argument("-rt", help = "If you use this parameter, the app will fetch retweets as well", action = "store_true")
	args = vars(parser.parse_args())

	user_to_fetch = args["u"]
	gets_rts = args["rt"]

	# The flow is very simple: we initialize the API, we get the data, and then we write the data
	api = initializeAPI()
	tweets = obtain_tweets(api, user_to_fetch, gets_rts)
	write_data_to_file(tweets, user_to_fetch + ".txt")

	exit(0)

if __name__ == "__main__":
	main()
