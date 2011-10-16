# tweets.py
# A simple example of pulling in and printing the last 20 tweets from the public timeline. It uses the package: tweepy
#
# You might need to do: [sudo] easy_install tweepy

import tweepy

api = tweepy.API()

timeline = api.public_timeline()

for i in timeline:
    print i.text
