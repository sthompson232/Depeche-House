from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

#DATABASE MODELS

#TABLE CONTAINING ALL USER INFORMATION IN THE SQLITE DATABASE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), index=True, unique=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

#METHOD TO SET HASHED PASSWORD (USED WHEN FIRST REGISTERING A PASSWORD)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

#METHOD TO CHECK HASHED PASSWORD (USED WHEN LOGGING IN)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)