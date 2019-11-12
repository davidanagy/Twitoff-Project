# Twitoff-Project
Writing a web application for comparing and predicting tweets

Currently contains the following files (all in the TWITOFF folder):

1. __init__.py: Entry point for the app.

2. app.py: Code for the app. Currently gives a list of users in the database,
with hyperlinks that take you to a page that lists their tweets in the database.

3. models.py: Creates classes for the database that contains the tweet data.

4. twitter.py: Code that enables one to insert user and tweet data into the database,
as long as one has the requisite Twitter API keys (and Basilica key). Use the "add_user"
function to add new users to the database.

5. fake_data.py: Code for creating fake data and inserting it into the database.

6. db.sqlite3: Database; currently contains data for the following Twitter accounts:
* [@sadserver](https://twitter.com/sadserver)
* [@dril](https://twitter.com/dril)
* [@realDonaldTrump](https://twitter.com/realDonaldTrump)
* [@theshrillest](https://twitter.com/theshrillest)
* [@HaleyOSomething](https://twitter.com/HaleyOSomething)
* [@LAClippers](https://twitter.com/LAClippers)
* [@Chiney321](https://twitter.com/Chiney321)
* [@BernieSanders](https://twitter.com/BernieSanders)

7. A "templates" folder that contains HTML templates for the app's pages.
Currently contains two templates:
* "base.html," for the homepage and a convenient way to reset the database;
* "user_tweets.html," for displaying the tweets of each user.