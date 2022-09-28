from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask import current_app as app
from .models import Trade
from .forms import TradeForm, UpdateTradeForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from tradingjournal import db
from tradingjournal.tools import allowed_file, csv_import

trades_bp = Blueprint("trades_bp", __name__)

dateformat = "%Y-%m-%d"


@app.route("/trade/add", methods=["GET", "POST"])
#@db_add_limit
def add_trade():
    """
    Return existing and add new trades.
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

        return redirect(url_for("add_trade"))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_trade.html", form=form, title="Trades")


@app.route("/trade/import", methods=["GET", "POST"])
def import_trade():
    """
    Return page used to import trades from a CSV file.
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


@app.route("/trade/update/<ref>", methods=["GET", "POST"])
def update_trade(ref):
    """
    Update an existing trade in the database.
    """

    trade = Trade.query.filter_by(id=ref).first()
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


@app.route("/trade/delete", methods=["POST"])
def delete_trade():
    """
    Update an exiting trade in the database.
    """

    try:
        trade = Trade.query.filter_by(id=request.form["ref"]).first()
        db.session.delete(trade)
        db.session.commit()
        flash("Delete successful.", "danger")

    except:
        db.session.rollback()
        flash("Error deleting trade.", "danger")

    return redirect(url_for("index"))

