from flask import current_app as app
from flask import render_template, Blueprint, request
from .forms import RiskCalculator

risk_bp = Blueprint(
    "risk_bp", __name__, template_folder="templates", static_folder="static"
)




@app.route("/risk", methods=["GET", "POST"])
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
