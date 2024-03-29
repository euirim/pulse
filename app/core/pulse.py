import math
import tweepy

from .twitter import get_twitter_data


class KeyphraseRecordPool:
    def __init__(self, collection_interval=60):
        self.keyphrase_records = []
        self.collection_interval = collection_interval

    def fill(self, keyphrases):
        """
        Fill the pool with Keyphrase objects using given list of keyphrases.

        Input:
        keyphrases: [List string]
        """
        # to prevent API problems
        assert len(keyphrases) < 100

        keyphrases = list(map(lambda x: (x[0].lower(), x[1]), keyphrases))

        # get Twitter scores
        twitter_data = get_twitter_data(
            keyphrases, 
            self.collection_interval
        )

        # TODO: get keyphrase data from Facebook
        # TODO: get keyphrase data from Instagram
        # TODO: get keyphrase data from Reddit

        for kp in keyphrases:
            self.keyphrase_records.append(
                KeyphraseRecord(
                    keyphrase=kp[0],
                    fb={},
                    twitter=twitter_data[kp[0]],
                    instagram={},
                    reddit={}
                )
            )

    def get_scores(self):
        """
        Return a list of tuples, each with a keyword and its 
        associated score.
        """
        scores = []
        for kp in self.keyphrase_records:
            scores.append((kp.name, kp.twitter))

        return scores

        
class KeyphraseRecord:
    def __init__(self, keyphrase, fb, twitter, instagram, reddit):
        self.keyphrase = keyphrase
        self.fb = fb
        self.twitter = twitter
        self.instagram = instagram
        self.reddit = reddit

    def serialize_payload(self):
        return {
            'twitter': self.twitter.serialize(),
        }


if __name__=='__main__':
    keyphrases = ['donald trump', 'bernie sanders']
    pool = KeyphraseRecordPool(collection_interval=30)
    pool.fill(keyphrases)
    print(pool.get_scores())