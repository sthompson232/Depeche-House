from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user

from models import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'enter_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///depeche_house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#turns debug mode on if running with python
if __name__ =='__main__':
    app.run(debug=True)

#Allows users to login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#user loader keeps the user logged in during the session
@login_manager.user_loader
#LOADS THE USER
def load_user(user_id):
    return User.query.get(int(user_id))
    
###################################################################################################

#ROUTES


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
        flash("Congratulations, you have registered an account successfully.")
    return render_template('register.html', register_form=register_form)



#LOGIN PAGE ROUTE
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
            flash("Logged in successfully.")
        else:
            flash('Login Unsuccessful.')
    return render_template('login.html', login_form=login_form)



#INDEX HOME PAGE, THIS IS THE ONLY PAGE THAT DOESNT REQUIRE AN ACCOUNT
@app.route('/', methods=["GET", "POST"])
def index():
    current_users = User.query.all()
    return render_template('index.html', current_users=current_users)



#LOGOUT ROUTE WHICH AUTO REDIRECTS ON LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



#ROUTE FOR USER AREA
@app.route('/user', methods=["GET", "POST"])
@login_required
def user():
    return render_template('user.html')