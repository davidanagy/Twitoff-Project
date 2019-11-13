# Twitoff-Project
Writing a web application for comparing and predicting tweets.

Currently contains the following files (all in the TWITOFF folder).
Code that was added/changed on November 13 is in bold.

1. __init__.py: Entry point for the app.

2. app.py: Code for the app. **Lets you add users to the database,**
see their tweets, **and predict which of two users is more likely**
**to tweet a given string of text. (There's also an option to reset the database.)**

3. fake_data.py: Code for creating fake data and inserting it into the database.

4. models.py: Creates classes for the database that contains the tweet data.

5. **predict.py: Code that contains the machine learning model that makes the prediction.**

6. twitter.py: Code that enables one to insert user and tweet data into the database,
as long as one has the requisite Twitter API keys (and Basilica key). Use the "add_user"
function to add new users to the database.

7. db.sqlite3: The database for the app's backend.

8. A "templates" folder that contains HTML templates for the app's pages.
Currently contains the following templates:
* "base.html" **sets the framework for all pages, and contains code for the app's homepage.**
* **"prediction.html" is the page that displays the prediction.**
* **"reset_confirm.html" confirms whether or not to wipe the database of all data.**
* **"reset.html" is the page we see after we wipe the database.**
* "user_tweets.html" is currently deprecated, but I kept it in for my personal reference.
* "user.html" shows all the tweets in the database for a given user **in a convenient table format**.