"""Entry point for our Twitoff Flask app"""

from .app import create_app

# APP is a global variable
APP = create_app()

# run this in terminal with FLASK_APP=TWITOFF:APP flask run
