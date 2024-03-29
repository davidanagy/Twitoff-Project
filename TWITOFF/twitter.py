"""
Retrieve tweets and embeddings, and save into a database
"""

import basilica
from decouple import config
from .models import DB, Tweet, User
import tweepy


TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET_KEY'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))


def add_user(username, num_tweets=200, exclude_replies=True,
             include_rts=False, tweet_mode='extended'):
    """Add or update a user and their tweets, or else give an error"""
    try:
        user = TWITTER.get_user(username)
        profile = user.profile_image_url
        tweets = user.timeline(count=num_tweets,
                               exclude_replies=exclude_replies,
                               include_rts=include_rts, tweet_mode=tweet_mode)
        tweets_text = [tweet.full_text for tweet in tweets]
        embedding = BASILICA.embed_sentences(tweets_text, model='twitter')
        db_user = (User.query.get(user.id) or
                   User(id=user.id, name=username, profile=profile,
                        embedding=list(embedding)))
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300])
            DB.session.add(db_tweet)
            db_user.tweets.append(db_tweet)
        DB.session.add(db_user)

    except Exception as e:
        print(f'Error processing {username}: {e}')
        raise e
    else:
        DB.session.commit()
