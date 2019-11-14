"""These are my database models"""

from flask_sqlalchemy import SQLAlchemy


# Import a database; capital for global scope
DB = SQLAlchemy()


# Define User table and Tweet table
class User(DB.Model):
    """Twitter useres that we analyze"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    profile = DB.Column(DB.String(200), nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)
    embedding = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class Tweet(DB.Model):
    """The user's tweets from Twitter"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet {self.text}>'
