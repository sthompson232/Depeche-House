from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


#ADD POST FORM

class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('What would you like to say?', validators=[DataRequired()])
    submit = SubmitField('Post')
