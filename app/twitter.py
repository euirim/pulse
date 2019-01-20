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
        status_text = extract_status_text(status)

        self.tweets.append(status)
        if (time.time() - self.start_time) > self.limit:
            return False

    def on_error(self, status):
        print(status)


def extract_status_text(status):
    """
    Get full text of given twitter status.
    """
    try:
        return status._json['retweeted_status']['extended_tweet']['full_text']
    except KeyError:
        try:
            return status._json['retweeted_status']['text']
        except KeyError:
            try:
                return status._json['extended_tweet']['full_text']
            except KeyError:
                return status.text


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

    listener = TwitterStreamListener(time_limit=60)
    stream = tweepy.Stream(
        auth=api.auth, 
        listener=listener 
    )

    stream.filter(track=keyphrases, languages=['en'])

    # Initialize scores
    scores = {}
    for kp in keyphrases:
        scores[kp] = 0

    for tweet in listener.tweets: 
        tweet_text = extract_status_text(tweet).lower()
        for kp in keyphrases:
            if kp in tweet_text:
                scores[kp] += tweet.retweet_count + tweet.favorite_count + 1

    return scores