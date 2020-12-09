from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from depeche_house.users.forms import LoginForm, RegistrationForm, UpdateProfileForm
from depeche_house.models import User
from depeche_house import db
from depeche_house.users.utils import save_profile_pic

users = Blueprint('users', __name__)



@users.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        flash(f'Congratulations {register_form.username.data}, you have successfully registered an account.', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', register_form=register_form)



#LOGIN PAGE ROUTE
@users.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    login_form = LoginForm()
    #if necessary info has been submitted on login form:
    if login_form.validate_on_submit():
        #new variable finds row with submitted email
        user = User.query.filter_by(email=login_form.email.data).first()
        #if password matches the given email then line after logs user in
        if user and user.check_password(login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash("Logged in successfully.", 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check Username and Password.', 'danger')
    return render_template('login.html', login_form=login_form)



    #LOGOUT ROUTE WHICH AUTO REDIRECTS ON LOGOUT
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



#ROUTE FOR USER AREA
@users.route('/user', methods=["GET", "POST"])
@login_required
def user():
    update_form = UpdateProfileForm()
    # IF FORM HAS REQUIRED INFORMATION
    if update_form.validate_on_submit():
        # IF THE PROFILE PICTURE WAS UPDATED
        if update_form.profile_pic.data:
            # NEW VARIABLE CALLING THE SAVE PROFILE PIC FUNCTION
            picture_file = save_profile_pic(update_form.profile_pic.data)
            # UPDATING THE DB WITH THE NEW PROFILE PIC
            current_user.profile_pic = picture_file
        # UPDATE USERNAME AND EMAIL ON THE DB
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        # FLASH MESSAGE AND REDIRECT
        flash('Your account has successfully been updated!', 'success')
        return redirect (url_for('users.user'))
    # IF THERE IS NO POST METHOD THEN JUST GET THE CURRENT USERNAME AND EMAIL IN THE FORM FIELDS
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('user.html', image_file=image_file, update_form=update_form)