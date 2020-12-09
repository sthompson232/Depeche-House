from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = '64c56f84624a5da4f7e8d386049ef370'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///depeche_house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Allows users to login
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)
login_manager.login_view = 'login'


#turns debug mode on if running with python
if __name__ =='__main__':
    app.run(debug=True)



from depeche_house.users.routes import users
from depeche_house.posts.routes import posts
from depeche_house.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)