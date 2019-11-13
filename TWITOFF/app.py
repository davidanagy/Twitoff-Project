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
                message = f'User {name} successfully added!'
            else:
                message = f"Here are {name}'s most recent tweets:"
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []
        return render_template('user.html', title=name,
                               tweets=tweets, message=message)

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
        return render_template('prediction.html', title='Prediction',
                               message=message)

    return app
