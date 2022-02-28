from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5


app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///journal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "igeuHGFFk773VAUEn2bcwim3"
app.config["UPLOAD_FOLDER"] = "./app/uploads"
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

db = SQLAlchemy(app)

# late import so modules can import their dependencies properly
from . import models, views, forms

db.create_all()
