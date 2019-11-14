"""Build my app factory and do routes and configuration"""

from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_user


load_dotenv()

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

    # adding in a new route to add and get users
    @app.route('/user', methods=['POST'])  # users form
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_user(name)
                message1 = 'User'
                message2 = ' successfully added!'
            else:
                message1 = 'These are'
                message2 = "'s most recent tweets."
            query = User.query.filter(User.name == name).one()
            tweets = query.tweets
            profile = query.profile
        except Exception as e:
            message1 = 'Error adding'
            message2 = f': {e}'
            tweets = []
        return render_template('user.html', title=name,
                               tweets=tweets, message1=message1,
                               message2=message2, profile=profile)

    @app.route('/reset')
    @app.route('/reset/confirm')
    def reset():
        if request.path == '/reset/confirm':
            return render_template('reset_confirm.html',
                                   title='Reset Confirmation')
        else:
            DB.drop_all()
            DB.create_all()
            return render_template('reset.html', title='Reset')

    # adding in a route for predictions
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves'
        else:
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'])
            message = '"{}" is more likely to be tweeted by {} than {}. \
                      Therefore, {} wins!'.format(
                      request.values['tweet_text'],
                      user1 if prediction else user2,
                      user2 if prediction else user1,
                      user1 if prediction else user2)
            query1 = User.query.filter(User.name == user1).one()
            query2 = User.query.filter(User.name == user2).one()
            profile1 = query1.profile
            profile2 = query2.profile
        return render_template('prediction.html', title='Prediction',
                               message=message,
                               profile1=profile1, profile2=profile2)

    return app
