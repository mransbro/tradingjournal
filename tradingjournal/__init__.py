from flask import Flask
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from os import environ
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()


def init_app():
    app = Flask(__name__)

    key = environ.get("SECRET_KEY", "qwertyuiop")
    app.config["SECRET_KEY"] = key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///journal.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "tradingjournal/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

    db.init_app(app)
    bootstrap = Bootstrap5(app)

    with app.app_context():

        from .home import home
        from .trades import trades
        from .risk import risk

        app.register_blueprint(home.home_bp)
        app.register_blueprint(trades.trades_bp)
        app.register_blueprint(risk.risk_bp)


        #limiter = Limiter(app, default_limits=["15/minute"], key_func=get_remote_address)
        #limiter = Limiter(app, default_limits=["15/minute"], key_func=get_remote_address)

        return app
