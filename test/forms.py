from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from test.models import User, Player


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'{username.data} is already taken please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
             raise ValidationError(f'{email.data} is already taken please choose another one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'{username.data} is already taken please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'{email.data} is already taken please choose another one.')


class PlayerForm(FlaskForm):
    player_name = StringField('Player Name', validators=[DataRequired()])
    player_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    player_style = StringField('Playing Style', validators=[DataRequired()])
    player_stats = StringField('Player Stats')
    player_average = StringField('Player Average')
    player_country = StringField('Player Country')
    submit = SubmitField('Save')