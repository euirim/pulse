import os
import time
import tweepy


class TwitterRecord:
    def __init__(
        self, 
        keyphrase,
        tweet_count, 
        fav_count, 
        retweet_count, 
        reply_count
    ):
        self.keyphrase = keyphrase
        self.tweet_count = tweet_count
        self.fav_count = fav_count
        self.retweet_count = retweet_count
        self.reply_count = reply_count

    def serialize(self):
        return {
            'tweet_count': self.tweet_count,
            'fav_count': self.fav_count,
            'retweet_count': self.retweet_count,
            'reply_count': self.reply_count
        }


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

    def get_records(self, keyphrases):
        records = {}
        for kp in keyphrases:
            records[kp] = TwitterRecord(
                keyphrase=kp,
                tweet_count=0,
                fav_count=0,
                retweet_count=0,
                reply_count=0
            )

        for tweet in self.tweets: 
            tweet_text = extract_status_text(tweet).lower()
            for kp in keyphrases:
                if kp in tweet_text:
                    records[kp].tweet_count += 1
                    records[kp].fav_count += tweet.retweet_count
                    records[kp].retweet_count += tweet.favorite_count
                    records[kp].reply_count += tweet.reply_count

        return records


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


def get_twitter_data(keyphrases, collection_interval):
    auth = tweepy.OAuthHandler(
        os.environ['PULSE_TWITTER_CONSUMER_TOKEN'], 
        os.environ['PULSE_TWITTER_CONSUMER_SECRET']
    )
    auth.set_access_token(
        os.environ['PULSE_TWITTER_ACCESS_TOKEN'], 
        os.environ['PULSE_TWITTER_ACCESS_TOKEN_SECRET']
    )
    api = tweepy.API(auth)

    listener = TwitterStreamListener(time_limit=collection_interval)
    stream = tweepy.Stream(
        auth=api.auth, 
        listener=listener 
    )

    stream.filter(track=keyphrases, languages=['en'])

    records = listener.get_records(keyphrases)

    return records