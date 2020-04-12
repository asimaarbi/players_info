from datetime import datetime
from test import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(25), nullable=False)
    player_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    player_style = db.Column(db.String(10), nullable=False)
    player_stats = db.Column(db.String(10), nullable=True)
    player_average = db.Column(db.String(10), nullable=True)
    player_country = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return f"Player('{self.player_name}', '{self.player_image}', '{self.player_style}'," \
               f" '{self.player_stats}', '{self.player_average}', '{self.player_country}')"