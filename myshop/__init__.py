from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'youwontguessthis'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
Bootstrap = Bootstrap(app)
logM = LoginManager(app)

from myshop import routes