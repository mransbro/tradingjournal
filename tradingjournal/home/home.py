from flask import Blueprint
from flask import render_template
from sqlalchemy import desc
from tradingjournal.trades.models import Trade

home_bp = Blueprint(
    "home_bp", __name__, template_folder="templates", static_folder="static"
)

dateformat = "%Y-%m-%d"


@home_bp.route("/", methods=["GET"])
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
