from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'enter_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///depeche_house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Allows users to login
login_manager = LoginManager()
login_manager.init_app(app)

###################################################################################################

#DATABASE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), index=True, unique=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


####################################################################################################

#FORMS
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


####################################################################################################

#user loader keeps the user logged in during the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#ROUTES


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegistrationForm()
    #if necessary info has been submitted on the register form:
    if register_form.validate_on_submit():
        #new user will be added to the db with username and email of form data
        new_user = User(username=register_form.username.data, email=register_form.email.data)
        #use the class method for password as it needs to be hashed
        new_user.set_password(register_form.password.data)
        #add and commit the db change 
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index', _external=True, _scheme='http'))
    return render_template('register.html', register_form=register_form)



@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    #if necessary info has been submitted on login form:
    if login_form.validate_on_submit():
        #new variable finds row with submitted email
        user = User.query.filter_by(email=login_form.email.data).first()
        #if password matches the given email then line after logs user in
        if user and user.check_password(login_form.password.data):
            login_user(user)
            return redirect(url_for('index', _external=True, _scheme='http'))
    return render_template('login.html', login_form=login_form)



@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)