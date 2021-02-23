import asyncio
import sys
from channels.consumer import AsyncConsumer
from .models import Tweet
import json
import tweepy


# Get authentication keys from file
f = open("heatmap/keys.txt", "r")

# == OAuth Authentication ==
consumer_key = f.readline().rstrip()
consumer_secret = f.readline().rstrip()
access_token = f.readline().rstrip()
access_token_secret = f.readline().rstrip()

f.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tweet_queue = []

class StreamListener(tweepy.StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()

    def on_connect(self):
        print("Connected to streaming API")

    def on_data(self, data):
        try:
            # Get data from tweet
            datajson = json.loads(data)
            # created_at = datajson["created_at"]
            
            if(datajson["coordinates"]):
                # Coordinates from tweet
                coordinates = datajson["coordinates"]["coordinates"]
                latitude = coordinates[1]
                longitude = coordinates[0]

                # Check if latitude and longitude are floats
                if(isinstance(latitude, float) and isinstance(longitude, float)):
                    new_tweet = Tweet(latitude = latitude, longitude = longitude)
                    hashtags = datajson["entities"]["hashtags"]
                    text = []
                    for hashtag in hashtags:
                        text.append(hashtag["text"].lower())
                    new_tweet.hashtags = text
                    new_tweet.save()
                    if(len(Tweet.objects.all()) > 100000):
                        tweets = Notification.objects.all()[:90000]
                        Tweet.objects.exclude(pk__in=list(tweets)).delete() 
            return True
        except Exception as e:
            print(e)

    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return False
        # return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return False
        # return True # Don't kill the stream

class myConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

        # Streams tweets from box around Los Angeles, CA area
        GEOBOX_LA = [-119.2279,33.4263,-116.8997,34.7189]
        GEOBOX_CA = [-125.94,32.29,-113.68,42.67]
        GEOBOX_US = [-133.3,21.8,-60.4,51.3]
        sapi = tweepy.streaming.Stream(auth, StreamListener()) 
        sapi.filter(locations=GEOBOX_US, is_async=True)

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)