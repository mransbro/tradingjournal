from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField, IntegerField, HiddenField, BooleanField
from wtforms.validators import InputRequired, NumberRange, Regexp
from datetime import datetime

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///journal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "igeuHGFFk773VAUEn2bcwim3"

db = SQLAlchemy(app)

# Date format in YYYY-MM-DD
dateregex = "^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$"


# initialize database
def create_db():
    db.create_all()


class DailyJournal(db.Model):
    __tablename__ = "dailyjournal"
    date = db.Column(db.Date, primary_key=True)
    stocks_above_20ma = db.Column(db.Integer, unique=False, nullable=True)
    stocks_above_50ma = db.Column(db.Integer, unique=False, nullable=True)
    stocks_above_200ma = db.Column(db.Integer, unique=False, nullable=True)


class WeeklyJournal(db.Model):
    __tablename__ = "weeklyjournal"
    date = db.Column(db.Date, primary_key=True)
    industry_groups = db.Column(db.String, nullable=True)
    scans = db.Column(db.Boolean, default=False, server_default="False")
    watchlist = db.Column(db.Boolean, default=False, server_default="False")
    focuslist = db.Column(db.Boolean, default=False, server_default="False")
    open_positions = db.Column(db.Boolean, default=False, server_default="False")


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
                dateregex,
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
                dateregex,
                message="Invalid date format",
            ),
        ],
    )
    industry_groups = StringField("Record notable changes of industry groups")
    scans = BooleanField("Review weekly scans")
    watchlist = BooleanField("Review Watchlist")
    focuslist = BooleanField("Create Focuslist")
    open_positions = BooleanField("Open positions")
    submit = SubmitField("Submit")


class TradeForm(FlaskForm):
    date = StringField(
        "Date (YYYY-MM-DD)",
        validators=[
            InputRequired(),
            Regexp(
                dateregex,
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
            NumberRange(min=0, max=10000, message="Invalid number"),
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
    submit = SubmitField("Submit")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_dailyroutine", methods=["GET", "POST"])
def add_dailyjournal():

    entries = DailyJournal.query
    form = DailyForm()

    if form.validate_on_submit():

        record = DailyJournal(
            date=datetime.strptime(form.date.data, "%Y-%m-%d"),
            stocks_above_20ma=form.stocks_above_20ma.data,
            stocks_above_50ma=form.stocks_above_50ma.data,
            stocks_above_200ma=form.stocks_above_200ma.data,
        )

        db.session.add(record)
        db.session.commit()

        message = f"The data for {record.date} has been submitted."

        return render_template("add_dailyjournal.html", message=message)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_dailyjournal.html", form=form, entries=entries)


@app.route("/add_weeklyroutine", methods=["GET", "POST"])
def add_weeklyjournal():

    entries = WeeklyJournal.query
    form = WeeklyForm()

    if form.validate_on_submit():

        record = WeeklyJournal(
            date=datetime.strptime(form.date.data, "%Y-%m-%d"),
            industry_groups=form.industry_groups.data,
            scans=form.scans.data,
            watchlist=form.watchlist.data,
            focuslist=form.focuslist.data,
            open_positions=form.open_positions.data,
        )

        db.session.add(record)
        db.session.commit()

        message = f"The data for {record.date} has been submitted."

        return render_template("add_weeklyjournal.html", message=message)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_weeklyjournal.html", form=form, entries=entries)


@app.route("/add_trade", methods=["GET", "POST"])
def add_trade():

    entries = Trade.query
    form = TradeForm()

    if form.validate_on_submit():

        record = Trade(
            date=datetime.strptime(form.date.data, "%Y-%m-%d"),
            symbol=form.symbol.data.upper(),
            position_size=form.position_size.data,
            net_pnl=form.net_pnl.data,
            net_roi=form.net_roi.data,
            notes=form.notes.data,
        )

        db.session.add(record)
        db.session.commit()

        message = f"The data for {record.symbol} has been updated"

        return render_template("add_trade.html", message=message, form=form)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_trade.html", form=form, entries=entries)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")