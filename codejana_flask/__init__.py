
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)

db = SQLAlchemy(app)


app.config['SECRET_KEY']='thisisfirstflaskapp'
#for Sqlite data base Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/cjflask.db'

#for PostgresSQl  database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cjpostgres:root@localhost:5432/cjflaskapp'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'biswaranjanroul56@gmail.com'
app.config["MAIL_PASSWORD"] = 'Rina@8093'

mail = Mail(app)

from codejana_flask import routes