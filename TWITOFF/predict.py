"""Prediction of users based on tweet embeddings"""

import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA


def predict_user(username1, username2, tweet_text, cache=None):
    """determine and return which user is more likely to tweet a phrase"""
    user_set = pickle.dumps((username1, username2))
    if cache and cache.exists(user_set):
        log_reg = pickle.loads(cache.get(user_set))
    else:
        # get the users
        user1 = User.query.filter(User.name == username1).one()
        user2 = User.query.filter(User.name == username2).one()
        # get the embeddings for the tweets of those users
        user1_embeddings = user1.embedding
        user2_embeddings = user2.embedding
        # split those into an erray
        embeddings = np.vstack([user1_embeddings, user2_embeddings])
        labels = np.concatenate([np.ones(len(user1.tweets)),
                                 np.zeros(len(user2.tweets))])
        # fit the Logistic Regression model
        log_reg = LogisticRegression().fit(embeddings, labels)
        cache and cache.set(user_set, pickle.dumps(log_reg))
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
