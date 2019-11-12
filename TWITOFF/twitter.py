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


# Define function to add a new user and their tweets to the database
def add_user(username, num_tweets=200, exclude_replies=True,
             include_rts=False, tweet_mode='extended'):
    user = TWITTER.get_user(username)
    tweets = user.timeline(count=num_tweets, exclude_replies=exclude_replies,
                           include_rts=include_rts, tweet_mode=tweet_mode)
    db_user = User(id=user.id, name=user.screen_name,
                   newest_tweet_id=tweets[0].id)

    for tweet in tweets:
        embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500],
                         embedding=embedding)
        DB.session.add(db_tweet)
        db_user.tweets.append(db_tweet)
 
    DB.session.add(db_user)
    DB.session.commit()
