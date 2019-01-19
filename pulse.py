import math
import tweepy

from twitter import get_twitter_scores


class KeyphrasePool:
    def __init__(self):
        self.keyphrases = []

    def fill(self, keyphrases):
        """
        Fill the pool with Keyphrase objects using given list of keyphrases.

        Input:
        keyphrases: [List string]
        """
        # to prevent API problems
        assert len(keyphrases) < 100

        # get Twitter scores
        twitter_scores = get_twitter_scores(keyphrases)

        # TODO: get scores from Facebook
        # TODO: get scores from Instagram
        # TODO: get scores from Reddit
        
        for kp in keyphrases:
            self.keyphrases.append(
                Keyphrase(
                    name=kp,
                    fb={},
                    twitter=twitter_scores[kp],
                    instagram={},
                    reddit={}
                )
            )


    def get_scores(self):
        """
        Return a list of tuples, each with a keyword and its 
        associated score.
        """
        assert len(self.keyphrases) > 0

        scores = []
        for kp in self.keyphrases:
            scores.append((kp.name, kp.twitter))

        return scores

        
class Keyphrase:
    def __init__(self, name, fb, twitter, instagram, reddit):
        self.name = name
        self.fb = fb
        self.twitter = twitter
        self.instagram = instagram
        self.reddit = reddit

    def calc_score(self):
        return 0


def main():
    keyphrases = ['donald trump', 'bernie sanders']
    pool = KeyphrasePool()
    pool.fill(keyphrases)
    print(pool.get_scores())


if __name__=='__main__':
    main()