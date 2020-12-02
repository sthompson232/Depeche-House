from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf import FlaskForm
from flask_login import current_user
from depeche_house.models import User

#FORMS

#REGISTRATION FORM 
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=25)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            print("working")
            raise ValidationError('This username has already been taken. Please choose another one.')

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('This email has already been taken. Please choose another one.')

#LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

#UPDATE PROGILE FORM
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                print("working")
                raise ValidationError('This username has already been taken. Please choose another one.')

    def validate_email(self, email):
        if username.data != current_user.username:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email:
                raise ValidationError('This email has already been taken. Please choose another one.')