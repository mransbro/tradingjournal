from flask import Flask
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from os import environ

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap5(app)

key = environ.get("SECRET_KEY", "qwertyuiop")
app.config["SECRET_KEY"] = key


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///journal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "tradingjournal/uploads"
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024


# late import so modules can import their dependencies properly
from tradingjournal import models, views, forms
