from . import db
from .models import Trade
from datetime import datetime
from csv import reader

ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# initialize database
def create_db():
    db.create_all()


def csv_import(file="./sample_trades.csv"):

    with open(file) as filename:
        data = reader(filename)
        trades = list(data)

    for trade in trades[1:]:

        num_shares = float(trade[2])
        buy_price = float(trade[3])
        sell_price = float(trade[4])

        position_size = round(num_shares * buy_price, 2)
        net_pnl = round((num_shares * sell_price) - position_size, 2)
        net_roi = round(net_pnl / position_size * 100, 2)

        record = Trade(
            date=datetime.strptime(trade[0], "%Y-%m-%d"),
            symbol=trade[1].upper(),
            num_shares=num_shares,
            buy_price=buy_price,
            sell_price=sell_price,
            position_size=position_size,
            net_pnl=net_pnl,
            net_roi=net_roi,
            notes=trade[5],
        )

        db.session.add(record)
        db.session.commit()
