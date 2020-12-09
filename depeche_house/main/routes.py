from flask import Blueprint
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required
from depeche_house.models import User, Post


main = Blueprint('main', __name__)



#INDEX HOME PAGE, THIS IS THE ONLY PAGE THAT DOESNT REQUIRE AN ACCOUNT
@main.route('/')
def index():
    current_users = User.query.all()
    return render_template('index.html', current_users=current_users)



#ROUTE FOR PAGE WITH POSTS
@main.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    # POSTS ARE SORTED BY THEIR DATE IN DESCENDING ORDER. ALSO PAGINATED INTO PAGES
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)



