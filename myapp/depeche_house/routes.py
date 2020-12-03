from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, LoginManager, current_user
from depeche_house.forms import LoginForm, RegistrationForm, UpdateProfileForm, AddPostForm
from depeche_house.models import User, Post
from depeche_house import app, db
import os
from PIL import Image
import secrets

#Allows users to login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#user loader keeps the user logged in during the session
@login_manager.user_loader
#LOADS THE USER
def load_user(user_id):
    return User.query.get(int(user_id))


#ROUTES

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    return render_template('register.html', register_form=register_form)



#LOGIN PAGE ROUTE
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Username and Password.', 'danger')
    return render_template('login.html', login_form=login_form)



#INDEX HOME PAGE, THIS IS THE ONLY PAGE THAT DOESNT REQUIRE AN ACCOUNT
@app.route('/')
def index():
    current_users = User.query.all()
    return render_template('index.html', current_users=current_users)



#LOGOUT ROUTE WHICH AUTO REDIRECTS ON LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



#ROUTE FOR PAGE WITH POSTS
@app.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)



#FUNCTION TO ADD UPDATED PICTURE TO FILEPATH
def save_profile_pic(uploaded_pic):
    #create new name for uploaded picture
    random_hex = secrets.token_hex(4)
    pic_name = str(current_user.username) + random_hex
    #extracting the file extension (jpg or png) 
    _, f_ext = os.path.splitext(uploaded_pic.filename)
    #creating the new filename with the last two variables
    pic_filename = pic_name + f_ext
    #creating the picture path for it to be saved
    picture_path = os.path.join(app.root_path, 'static/profile_pics', pic_filename)
    #USING PILLOW. define new image size
    output_size = (100, 100)
    #open the image saved as a variable
    i = Image.open(uploaded_pic)
    #convert to RGB as png does not support RGBA
    rgb_i = i.convert('RGB')
    #add the new dimension size to the image
    rgb_i.thumbnail(output_size)
    #saving changes
    rgb_i.save(picture_path)
    #returning the new picture which has now been added to the static folder 
    return pic_filename



#ROUTE FOR USER AREA
@app.route('/user', methods=["GET", "POST"])
@login_required
def user():
    update_form = UpdateProfileForm()

    if update_form.validate_on_submit():
        if update_form.profile_pic.data:
            picture_file = save_profile_pic(update_form.profile_pic.data)
            current_user.profile_pic = picture_file
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        flash('Your account has successfully been updated!', 'success')
        return redirect (url_for('user'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('user.html', image_file=image_file, update_form=update_form)



#ADD POST PAGE
@app.route('/add-post', methods=["GET", "POST"])
@login_required
def add_post():
    post_form = AddPostForm()
    if post_form.validate_on_submit():
        new_post = Post(title=post_form.title.data, content=post_form.text.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('add_post.html', post_form=post_form)
