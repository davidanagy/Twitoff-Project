from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import TWITTER

# make an app factory

def create_app():
    app = Flask(__name__)

    # add config
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # have the database know about the app
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])

    @app.route('/user/<name>')
    def show_user_tweets(name):
        user = User.query.filter_by(name=name).first()
        tweets = Tweet.query.filter_by(user_id=user.id).all()
        return render_template('user_tweets.html', username=name, tweets=tweets)
    
    return app
