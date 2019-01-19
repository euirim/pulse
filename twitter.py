import os
import time
import tweepy


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit):
        super(TwitterStreamListener, self).__init__()
        self.start_time = time.time()
        self.limit = time_limit  # in seconds
        self.tweets = []

    def on_status(self, status):
        # accomodating weird twitter text truncation
        try:
            print(status._json['retweeted_status']['extended_tweet']['full_text'])
        except KeyError:
            try:
                print(status._json['retweeted_status']['text'])
            except KeyError:
                try:
                    print(status._json['extended_tweet']['full_text'])
                except KeyError:
                    print(status.text)

        self.tweets.append(status)
        if (time.time() - self.start_time) > self.limit:
            return False

    def on_error(self, status):
        print(status)


def get_twitter_scores(keyphrases):
    auth = tweepy.OAuthHandler(
        os.environ['PULSE_TWITTER_CONSUMER_TOKEN'], 
        os.environ['PULSE_TWITTER_CONSUMER_SECRET']
    )
    auth.set_access_token(
        os.environ['PULSE_TWITTER_ACCESS_TOKEN'], 
        os.environ['PULSE_TWITTER_ACCESS_TOKEN_SECRET']
    )
    api = tweepy.API(auth)

    listener = TwitterStreamListener(time_limit=30)
    stream = tweepy.Stream(
        auth=api.auth, 
        listener=listener, 
        tweet_mode='extended'
    )

    stream.filter(track=keyphrases, languages=['en'])

    scores = {}
    for kp in keyphrases:
        scores[kp] = len(listener.tweets)

    return scores