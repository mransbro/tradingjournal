from crypt import methods
from . import app, db
from .tools import allowed_file
from .models import WeeklyRoutine, DailyRoutine, Trade
from .forms import DailyForm, WeeklyForm, TradeForm
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from csv import reader
from datetime import datetime


@app.route("/")
def index():
    return render_template("index.html", title="Trading Journal")


@app.route("/add_dailyroutine", methods=["GET", "POST"])
def add_dailyroutine():

    form = DailyForm()

    if form.validate_on_submit():

        record = DailyRoutine(
            date=form.date.data,
            stocks_above_20ma=form.stocks_above_20ma.data,
            stocks_above_50ma=form.stocks_above_50ma.data,
            stocks_above_200ma=form.stocks_above_200ma.data,
        )

        db.session.add(record)
        db.session.commit()

        message = f"The data for {record.date} has been submitted."

        return render_template("add_dailyroutine.html", message=message, form=form)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_dailyroutine.html", form=form, title="Daily Routine")


@app.route("/add_weeklyroutine", methods=["GET", "POST"])
def add_weeklyroutine():

    form = WeeklyForm()

    if form.validate_on_submit():

        record = WeeklyRoutine(
            date=form.date.data,
            industry_groups=form.industry_groups.data,
            scans=form.scans.data,
            watchlist=form.watchlist.data,
            focuslist=form.focuslist.data,
            open_positions=form.open_positions.data,
        )

        db.session.add(record)
        db.session.commit()

        message = f"The data for {record.date} has been submitted."

        return render_template("add_weeklyroutine.html", message=message, form=form)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_weeklyroutine.html", form=form, title="Weekly Routine")


@app.route("/add_trade", methods=["GET"])
def add_trade():

    form = TradeForm()

    if form.validate_on_submit():

        record = Trade(
            date=form.date.data,
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

    return render_template("add_trade.html", form=form, title="Trades")


@app.route("/api/trade")
def trade_data():
    return {"data": [trade.to_dict() for trade in Trade.query.all()]}


@app.route("/api/daily")
def daily_data():
    return {
        "data": [dailyroutine.to_dict() for dailyroutine in DailyRoutine.query.all()]
    }


@app.route("/api/weekly")
def weekly_data():
    return {
        "data": [weeklyroutine.to_dict() for weeklyroutine in WeeklyRoutine.query.all()]
    }


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@app.errorhandler(404)
def handle_404(e):
    return "404", 404


@app.errorhandler(500)
def handle_500(e):
    return "500", 500


@app.route("/add_trade", methods=["POST"])
def upload():

    file = request.files["file"]

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(file.filename)

    with open(filename) as file:
        data = reader(file)
        trades = list(data)

    for trade in trades[1:]:
        record = Trade(
            date=datetime.strptime(trade[0], "%Y-%m-%d"),
            symbol=trade[1],
            position_size=trade[2],
            net_pnl=trade[3],
            net_roi=trade[4],
            notes=trade[5],
        )

        db.session.add(record)
        db.session.commit()
        # message = "Csv file has been uploaded"

    return redirect(url_for("add_trade"))
