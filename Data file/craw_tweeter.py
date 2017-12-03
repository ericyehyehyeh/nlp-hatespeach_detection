import tweepy
from tweepy import OAuthHandler
import json
import csv
 
consumer_key = 'yXpOUOhEAnj63UsvjTawzgDu8'
consumer_secret = 'tRkhVITN5RbsqQJlJDUcZwleQoElgAc3CE8zHSlY3RhDnz5Jwx'
access_token = '1621165346-tky1tilKqv0kLQDPDemxJcvt7t8VUYH2NkReVxk'
access_secret = 'OeXeykbRYKGNFBC6RK1CMqQz08KwTPNzzaAC2BUAaVUhI'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


with open('data_craw.csv', 'w') as csvfile:
    csvCursor = csv.writer(csvfile)
    csvHeader = ['tweet_text']
    csvCursor.writerow(csvHeader)
    username = 'realDonaldTrump'
    
    for tweet in tweepy.Cursor(api.user_timeline, screen_name = username).items():
        csvCursor.writerow([tweet.text])
