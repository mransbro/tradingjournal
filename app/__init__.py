from flask import Flask
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap5
from app.models import db
from config import Config
from app.tools import checkdb

migrate = Migrate()


def init_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    db.app = app

    migrate.init_app(app, db)
    migrate.app = app

    bootstrap = Bootstrap5(app)

    with app.app_context():

        from app.main import bp as main_bp

        db.create_all()

        app.register_blueprint(main_bp)

        checkdb()

        return app
