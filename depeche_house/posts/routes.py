from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import login_required, current_user
from depeche_house.posts.forms import AddPostForm
from depeche_house.models import Post
from depeche_house import db




posts = Blueprint('posts', __name__)


#ADD POST PAGE
@posts.route('/add-post', methods=["GET", "POST"])
@login_required
def add_post():
    post_form = AddPostForm()
    if post_form.validate_on_submit():
        #inputting values to db table
        new_post = Post(title=post_form.title.data, content=post_form.text.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('main.home'))
    return render_template('add_post.html', post_form=post_form, legend="Add Post")



@posts.route('/post/<int:post_id>', methods=["GET", "POST"])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)



@posts.route('/post/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    #if person clicking on link wasnt the author of the post then abort message
    if post.author != current_user:
        abort(403)
    #creating a new instance of the post form 
    update_form = AddPostForm()

    if update_form.validate_on_submit():
        post.title = update_form.title.data
        post.content = update_form.text.data
        db.session.commit()
        flash("Post Updated", 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == "GET":
        #makes post writing appear in the form inputs
        update_form.title.data = post.title
        update_form.text.data = post.content

    return render_template('add_post.html', post_form=update_form, legend="Update Post")



@posts.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", 'success')
    return redirect( url_for('main.home'))