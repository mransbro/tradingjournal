from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import InputRequired, Regexp, Optional
from flask_wtf import FlaskForm

letterregex = "^[a-zA-Z]+$"
dateregex = "^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$"


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
