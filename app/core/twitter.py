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
        }


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit):
        super(TwitterStreamListener, self).__init__()
        self.start_time = time.time()
        self.limit = time_limit  # in seconds
        self.tweets = []

    def on_status(self, status):
        # accomodating weird twitter text truncation
        status_text = extract_total_status_text(status)

        self.tweets.append(status)
        if (time.time() - self.start_time) > self.limit:
            return False

    def on_error(self, status):
        print(status)

    def get_records(self, keyphrases):
        records = {}
        for kp in keyphrases:
            records[kp[0]] = TwitterRecord(
                keyphrase=kp[0],
                tweet_count=0,
                fav_count=0,
                retweet_count=0,
                reply_count=0
            )

        print('Tweets Total Processed: {}'.format(len(self.tweets)))

        for tweet in self.tweets: 
            recorded = False
            tweet_text = extract_total_status_text(tweet).lower()
            for kp in keyphrases:
                if any(k.lower() in tweet_text for k in ([kp[0]] + kp[1])):
                    recorded = True
                    records[kp[0]].tweet_count += 1
                    records[kp[0]].fav_count += tweet.retweet_count
                    records[kp[0]].retweet_count += tweet.favorite_count
                    records[kp[0]].reply_count += tweet.reply_count

            if not recorded:
                print('TWEET NOT RECORDED:')
                print(tweet_text)
                print('-' * 60)

        return records


def extract_total_status_text(status):
    """
    Get full text of given twitter status, along with the text of its 
    immediately associated statuses (immediate retweets, immediate quotes).

    'Immediate' in this context means that we do not examine a quoted tweets own quotes.
    """
    status_texts = []

    # Get status text
    try: 
        status_texts.append(status._json['extended_tweet']['full_text'])
    except KeyError:
        status_texts.append(status.text) 
        
    # Get retweeted status text
    try:
        status_texts.append(
            extract_status_text(status._json['retweeted_status'])
        )
    except KeyError:
        pass 

    # Get quoted status text
    try:
        status_texts.append(extract_status_text(status._json['quoted_status']))
    except KeyError:
        pass 

    return " ".join(status_texts)


def extract_status_text(status_json):
    """
    Get full text of given twitter status (in JSON).
    """
    try:
        return status_json['extended_tweet']['full_text']
    except KeyError:
        return status_json['text'] 


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

    stream.filter(
        track=map(lambda x: x[0], keyphrases), 
        languages=['en']
    )

    records = listener.get_records(keyphrases)

    return records