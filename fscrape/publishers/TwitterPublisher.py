#!/usr/bin/python
import json as js
from pubsub import pub
from publishers.TwitterClient import Client
from messages.StandardMessage import StandardMessage

API_KEY, API_SECRET = ('5jquzflYqTUNMNqmpdxPUr4Si', 'RE3tNfpjyhNB5IJatzLiDnoonEw7i2OgWz0o5kSCbS2egllDBv')


class TwitterPublisher:
	def __init__(self, message, term):
		self.client = Client(API_KEY, API_SECRET)
		self.message_type = message
		self.search_term = term

		self.search_link_base = 'https://api.twitter.com/1.1/search/tweets.json?q='
		self.link_base = 'https://twitter.com/'
		print("publisher created")
		self.puiblish()

	#Get rate limit when the rate limit is less than the count given the system
	#must request rate_limit. Then enter waiting state

	def get_data(self, count):
		search_link = self.search_link_base + self.search_term + "&count=" + str(count)
		output = self.client.request(search_link)
		msg_array = []
		msg_array.append(self.get_rate())
		for x in range(len(output.get('statuses'))):
			msg = StandardMessage()
			msg.mentions = output.get('statuses')[x]['entities']['user_mentions']
			msg.id = output.get('statuses')[0]['id_str']
			msg.shares = str(output.get('statuses')[x]['retweet_count'])
			msg.likes = str(output.get('statuses')[x]['favorite_count'])
			msg.hashtags = output.get('statuses')[x]['entities']['hashtags']
			msg.url = self.link_base + output.get('statuses')[x]['user']['screen_name'] + '/status/' + msg.id
			msg.comment = str(output.get('statuses')[x]['text'])
			output.get('statuses')[x]['text']
			msg.shared = str(output.get('statuses')[x]['retweeted'])
			msg_array.append(msg)
		return msg_array

	def get_rate(self):
		i = self.client.rate_limit_status()['resources']['search']
		return i

	def puiblish(self):
		msg = self.get_data(100)
		for i in range(10):
			print('publish run: ' + str(len(msg)) + ' topic = ' + self.search_term)
			print(msg[1])
			pub.sendMessage(self.search_term, arg1=msg)

