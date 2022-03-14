from typing import Optional
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    HiddenField,
    BooleanField,
    FloatField,
)
from wtforms.validators import InputRequired, NumberRange, Regexp, Optional
from flask_wtf import FlaskForm


# Date format in YYYY-MM-DD
dateregex = "^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$"
letterregex = "^[a-zA-Z]+$"
numberregex = "^[0-9]+$"


class DailyForm(FlaskForm):
    id_field = HiddenField()
    date = StringField(id="datepick", validators=[Regexp(dateregex)])
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
    date = StringField(id="datepick", validators=[Regexp(dateregex)])
    industry_groups = StringField("Record notable changes of industry groups")
    scans = BooleanField("Review weekly scans")
    watchlist = BooleanField("Review Watchlist")
    focuslist = BooleanField("Create Focuslist")
    open_positions = BooleanField("Open positions")
    submit = SubmitField("Submit")


class TradeForm(FlaskForm):
    date = StringField(id="datepick", validators=[Regexp(dateregex)])
    symbol = StringField(
        "Symbol",
        validators=[
            InputRequired(),
            Regexp(letterregex, message="Invalid symbol format"),
        ],
    )
    num_shares = FloatField("No. of Shares")
    buy_price = FloatField("Buy Price")
    notes = StringField("Notes")
    submit = SubmitField("Submit")


class UpdateTradeForm(FlaskForm):
    date = StringField(id="datepick", validators=[Regexp(dateregex)])
    symbol = StringField(
        "Symbol",
        validators=[
            InputRequired(),
            Regexp(letterregex, message="Invalid symbol format"),
        ],
    )
    num_shares = FloatField("No. of Shares")
    buy_price = FloatField("Buy Price")
    sell_date = StringField(id="datepick", validators=[Optional(), Regexp(dateregex)])
    sell_price = FloatField("Sell Price", default=0, validators=[Optional()])
    notes = StringField("Notes")
    submit = SubmitField("Submit")


class RiskCalculator(FlaskForm):
    account_value = FloatField("Total account value")
    max_risk = FloatField("Max percent account risk")
    entry_price = FloatField("Entry price")
    stop = FloatField("Stop price")
    submit = SubmitField("Submit")
    num_shares = FloatField("Number of shares", default=0.0)
    position_size = FloatField("Total position size", default=0.0)
    risk_per_share = FloatField("Risk per share value", default=0.0)
    risk_account_percent = FloatField("Percent of risk for account", default=0.0)
    risk_account_value = FloatField("Total value of risk", default=0.0)
