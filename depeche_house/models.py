from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from depeche_house import db
from flask_login import UserMixin

#DATABASE

#TABLE CONTAINING ALL USER INFORMATION IN THE SQLITE DATABASE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True, nullable=False)
    profile_pic = db.Column(db.String(20), default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.joined_at}')"

#METHOD TO SET HASHED PASSWORD (USED WHEN FIRST REGISTERING A PASSWORD)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

#METHOD TO CHECK HASHED PASSWORD (USED WHEN LOGGING IN)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"