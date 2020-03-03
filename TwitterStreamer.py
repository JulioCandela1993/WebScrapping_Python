# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 08:20:26 2020

@author: juliochristian
"""

import os
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

os.chdir("G:/Documentos/MasterDegree/BDMA/Classes/UPC/CloudComputing/Lab3")

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('BrexitTweets.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

consumer_key = os.environ['CONSUMER-KEY']
consumer_secret = os.environ['CONSUMER-SECRET']
access_token = os.environ['ACCESS-TOKEN']
access_secret = os.environ['ACCESS-SECRET']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['Brexit'])