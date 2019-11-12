"""This code creates fake data for the database.
To use it, open a Flask shell in your terminal
and copy/paste this code into it."""

from .models import DB, Tweet, User


# create database
DB.create_all()

# create two users
u1 = User(name='austen')
u2 = User(name='davidanagyds')

# create six tweets
t1 = Tweet(text='wheeeee!!!!')
t2 = Tweet(text='sometimes people mistake me for the city :/')
t3 = Tweet(text='This is not a pipe')
t4 = Tweet(text='This week I learned how to make a Flask app! :D')
t5 = Tweet(text="can't wait for the clippers and lakers to both be 7-3 \
                 even though the clips are missing paul george")
t6 = Tweet(text='thinking of researching why there are \
                 so many libertarians in tech')

# put into lists for the for-loop
USERS = [u1, u2]
TWEETS = [t1, t2, t3, t4, t5, t6]

# add to database
for user in USERS:
    DB.session.add(user)

for tweet in TWEETS:
    DB.session.add(tweet)

# commit changes
DB.session.commit()