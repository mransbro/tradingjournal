from crypt import methods
from email.policy import default
from turtle import position
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    HiddenField,
    SelectField,
    RadioField,
    BooleanField,
)
from wtforms.validators import InputRequired, NumberRange, Regexp
from datetime import datetime

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entries.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "igeuHGFFk773VAUEn2bcwim3"

db = SQLAlchemy(app)


class DailyJournal(db.Model):
    __tablename__ = "dailyjournal"
    date = db.Column(db.Date, primary_key=True)
    stocks_above_20ma = db.Column(db.Integer, unique=False, nullable=True)
    stocks_above_50ma = db.Column(db.Integer, unique=False, nullable=True)
    stocks_above_200ma = db.Column(db.Integer, unique=False, nullable=True)

    def __init__(self, date, stocks_above_20ma, stocks_above_50ma, stocks_above_200ma):
        self.date = date
        self.stocks_above_20ma = stocks_above_20ma
        self.stocks_above_50ma = stocks_above_50ma
        self.stocks_above_200ma = stocks_above_200ma


class WeeklyJournal(db.Model):
    __tablename__ = "weeklyjournal"
    date = db.Column(db.Date, primary_key=True)
    watchlist = db.Column(db.Boolean)
    focuslist = db.Column(db.Boolean)
    open_positions = db.Column(db.Boolean)

    def __init__(self, date):
        self.date = date


class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    symbol = db.Column(db.String, nullable=False)
    position_size = db.Column(db.Integer, nullable=False)
    net_pnl = db.Column(db.Integer, default=0)
    net_roi = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, default="")


class DailyForm(FlaskForm):
    id_field = HiddenField()
    date = StringField(
        "Date (YYYY-MM-DD)",
        validators=[
            InputRequired(),
            Regexp(
                r"^((?:19|20)\\d\\d)-(0?[1-9]|1[012])-([12][0-9]|3[01]|0?[1-9])$",
                message="Invalid date format",
            ),
        ],
    )
    stocks_above_20ma = IntegerField(
        "Stocks above 20ma (%)",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100, message="Invalid number"),
        ],
    )
    stocks_above_50ma = IntegerField(
        "Stocks above 50ma (%)",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100, message="Invalid number"),
        ],
    )
    stocks_above_200ma = IntegerField(
        "Stocks above 200ma (%)",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100, message="Invalid number"),
        ],
    )
    submit = SubmitField("Submit")


class WeeklyForm(FlaskForm):
    date = StringField(
        "Date (YYYY-MM-DD)",
        validators=[
            InputRequired(),
            Regexp(
                r"^((?:19|20)\\d\\d)-(0?[1-9]|1[012])-([12][0-9]|3[01]|0?[1-9])$",
                message="Invalid date format",
            ),
        ],
    )
    watchlist = BooleanField("Watchlist")
    focuslist = BooleanField("Focuslist")
    open_positions = BooleanField("Open positions")
    submit = SubmitField("Submit")


class TradeForm(FlaskForm):
    date = StringField(
        "Date (YYYY-MM-DD)",
        validators=[
            InputRequired(),
            Regexp(
                r"^((?:19|20)\\d\\d)-(0?[1-9]|1[012])-([12][0-9]|3[01]|0?[1-9])$",
                message="Invalid date format",
            ),
        ],
    )
    symbol = StringField("Symbol")
    position_size = IntegerField("Position Size ($)")
    net_pnl = IntegerField(
        "Net P&L ($)",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100, message="Invalid number"),
        ],
    )
    net_roi = IntegerField(
        "Net ROI (%)",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100, message="Invalid number"),
        ],
    )
    notes = StringField("Notes")


# initialize database
def create_db():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_dailyroutine", methods=["GET", "POST"])
def add_dailyjournal():
    form = DailyForm()
    if form.validate_on_submit():
        date = datetime.strptime(request.form["date"], "%Y-%m-%d")
        stocks_above_20ma = request.form["stocks_above_20ma"]
        stocks_above_50ma = request.form["stocks_above_50ma"]
        stocks_above_200ma = request.form["stocks_above_200ma"]
        record = DailyJournal(
            date, stocks_above_20ma, stocks_above_50ma, stocks_above_200ma
        )
        db.session.add(record)
        db.session.commit()
        message = f"The data for {date} has been submitted."
        return render_template("add_record.html", message=message)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )
    return render_template("add_dailyjournal.html", form=form)


@app.route("/add_weeklyroutine", methods=["GET", "POST"])
def add_weeklyjournal():
    form = WeeklyForm()
    if form.validate_on_submit():
        date = datetime.strptime(request.form["date"], "%Y-%m-%d")
        watchlist = request.form["watchlist"]
        focuslist = request.form["focuslist"]
        open_positions = request.form["open positions"]
        record = WeeklyJournal(date, watchlist, focuslist, open_positions)
        db.session.add(record)
        db.session.commit()
        message = f"The data for {date} has been submitted."
        return render_template("add_record.html", message=message)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )
    return render_template("add_weeklyjournal.html", form=form)


@app.route("/add_trade")
def add_trade():
    form = TradeForm()
    if form.validate_on_submit():
        symbol = request.form["symbol"]
        record = Trade(date, symbol)
        db.session.add(record)
        db.session.commit()
        message = f"The data for {symbol} has been updated"
        return render_template("add_trade.html", message=message, form=form)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )
    return render_template("add_trade.html", form=form)
