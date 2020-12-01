from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'enter_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///depeche_house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#turns debug mode on if running with python
if __name__ =='__main__':
    app.run(debug=True)



from depeche_house import routes
from depeche_house.models import User