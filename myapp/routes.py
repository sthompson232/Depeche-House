from app import app, db, login_manager
from flask import request, render_template, flash, redirect,url_for
from models import User
from flask_login import current_user, login_user, logout_user, login_required
from forms import RegistrationForm,LoginForm
from werkzeug.urls import url_parse


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm(csrf_enabled=False)
    user = User.query.filter_by(email=login_form.email.data).first()
    if user and user.check_password(login_form.password.data):
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index', _external=True, _scheme='https'))
    else:
        return redirect(url_for('login', _external=True, _scheme='https'))
    return render_template('login.html', form=login_form)



@app.route('/user/<username>', methods=["GET", "POST"])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)
