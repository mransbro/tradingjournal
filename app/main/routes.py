from flask import render_template, flash, redirect, url_for, request
from app.models import Trade
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from app import db
from app.tools import allowed_file, csv_import
from app.main.forms import RiskCalculator, TradeForm, UpdateTradeForm
from app.main import bp
from sqlalchemy import desc

dateformat = "%Y-%m-%d"


@bp.route("/", methods=["GET"])
def index():
    """
    Return the homepage.
    """
    closedtrades = Trade.query.filter(Trade.sell_price != 0.0).all()
    opentrades = Trade.query.filter(Trade.sell_price == 0.0).all()
    latesttrades = (
        Trade.query.filter(Trade.sell_price != 0.0)
        .order_by(desc(Trade.date))
        .limit(10)
        .all()
    )

    latest_labels = [trade.date.strftime(dateformat) for trade in latesttrades]
    latest_values = [trade.net_roi for trade in latesttrades]

    roidata = [trade.net_roi for trade in closedtrades]
    wins = len([win for win in roidata if win > 0])
    loses = len(roidata) - wins
    winloss_labels = ["win", "loss"]
    winloss_values = [wins, loses]

    return render_template(
        "index.html",
        title="Trading Journal",
        winloss_labels=winloss_labels,
        winloss_values=winloss_values,
        latest_labels=latest_labels,
        latest_values=latest_values,
        opentrades=opentrades,
        closedtrades=closedtrades,
    )


@bp.route("/trade/add", methods=["GET", "POST"])
def add_trade():
    """
    Return existing and add new main.
    """

    form = TradeForm()

    if form.validate_on_submit():

        date = datetime.strptime(form.date.data, dateformat)
        symbol = form.symbol.data.upper()
        num_shares = form.num_shares.data
        buy_price = form.buy_price.data

        sell_date = None
        sell_price = 0.0
        position_size = round(num_shares * buy_price, 2)
        net_pnl = 0.0
        net_roi = 0.0

        record = Trade(
            date=date,
            symbol=symbol,
            num_shares=num_shares,
            buy_price=buy_price,
            sell_date=sell_date,
            sell_price=sell_price,
            position_size=position_size,
            net_pnl=net_pnl,
            net_roi=net_roi,
            notes=form.notes.data,
        )

        db.session.add(record)
        db.session.commit()
        flash("Trade successfully added.", "info")

        return redirect(url_for("main.add_trade"))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_trade.html", form=form, title="Trades")


@bp.route("/trade/import", methods=["GET", "POST"])
def import_trade():
    """
    Return page used to import main from a CSV file.
    """

    if request.method == "POST":

        if "file" not in request.files or request.files["file"] == "":
            flash("No file part", "warning")
            return redirect(request.url)

        file = request.files["file"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)

        csv_import(filename)
        os.remove(filename)

        flash("CSV file successfully imported.", "info")

        return render_template("import_trade.html")

    return render_template("import_trade.html")


@bp.route("/trade/update/<ref>", methods=["GET", "POST"])
def update_trade(ref):
    """
    Update an existing trade in the database.
    """

    trade = Trade.query.filter_by(ref=ref).first()
    form = UpdateTradeForm(obj=trade)

    if form.validate_on_submit():

        try:
            trade.date = datetime.strptime(form.date.data, dateformat)
            trade.symbol = form.symbol.data.upper()
            trade.num_shares = form.num_shares.data
            trade.buy_price = form.buy_price.data
            if not form.sell_date.data:
                trade.sell_date = None
            else:
                trade.sell_date = datetime.strptime(form.sell_date.data, dateformat)
            trade.sell_price = form.sell_price.data
            trade.position_size = round(form.num_shares.data * form.buy_price.data, 2)
            trade.notes = form.notes.data

            if form.sell_price.data == 0:
                trade.net_pnl = 0
                trade.net_roi = 0

            else:
                trade.net_pnl = round(
                    (form.num_shares.data * form.sell_price.data) - trade.position_size,
                    2,
                )
                trade.net_roi = round(trade.net_pnl / trade.position_size * 100, 2)

            db.session.add(trade)
            db.session.commit()
            flash("Trade updated successfully.", "success")

        except:
            db.session.rollback()
            flash("Error updating trade.", "danger")

    return render_template("update_trade.html", form=form)


@bp.route("/trade/delete", methods=["POST"])
def delete_trade():
    """
    Update an exiting trade in the database.
    """

    try:
        trade = Trade.query.filter_by(ref=request.form["ref"]).first()
        db.session.delete(trade)
        db.session.commit()
        flash("Delete successful.", "danger")

    except:
        db.session.rollback()
        flash("Error deleting trade.", "danger")

    return redirect(url_for("main.index"))


@bp.route("/risk", methods=["GET", "POST"])
def risk_calculator():
    """
    Risk calculator
    """

    form = RiskCalculator()
    risk = {}

    if request.method == "POST":

        if form.validate_on_submit():
            account_value = form.account_value.data
            max_risk = form.max_risk.data
            entry_price = form.entry_price.data
            stop = form.stop.data

            account_risk = account_value / 100 * max_risk
            trade_risk = entry_price - stop

            risk["risk_per_share"] = round(trade_risk, 2)
            risk["num_shares"] = round(account_risk / trade_risk, 2)
            risk["position_size"] = round(risk["num_shares"] * entry_price, 2)
            risk["risk_per_share_percent"] = round(
                (risk["risk_per_share"] / entry_price) * 100, 2
            )
            risk["risk_account_value"] = round(
                risk["num_shares"] * risk["risk_per_share"], 2
            )

        return render_template("risk_calculator.html", form=form, risk=risk)

    return render_template("risk_calculator.html", form=form, risk=risk)
