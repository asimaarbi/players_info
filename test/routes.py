import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from test import app, db, bcrypt
from test.forms import RegistrationForm, LoginForm, UpdateAccountForm, PlayerForm
from test.models import User, Player
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful for {form.username.data}.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check Username and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@app.route("/player")
def player():
    playerss = []
    players = Player.query.all()
    for player in players:
        image_file = url_for('static', filename='profile_pics/' + player.player_image)
        player.player_image = image_file
        playerss.append(player)
    return render_template('player.html', title='Player', players=playerss)


@app.route("/player/new", methods=['GET', 'POST'])
@login_required
def new_player():
    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(player_name=form.player_name.data, player_style=form.player_style.data,
                        player_stats=form.player_stats.data, player_average=form.player_average.data,
                        player_country=form.player_country.data)
        db.session.add(player)
        db.session.commit()
        flash('Player added successfully', 'success')
        return redirect(url_for('player'))
    return render_template('create_player.html', title='Player', form=form)


@app.route("/player_info/<uid>", methods=['GET', 'POST'])
def player_info(uid):
    players = []
    player = Player.query.get(uid)
    image_file = url_for('static', filename='profile_pics/' + player.player_image)
    player.player_image = image_file
    players.append(player)
    return render_template('player_info.html', title='Player Information', players=players)
