from app.models import Trade, db
from datetime import datetime
from csv import DictReader

ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def csv_import(file):

    csv = DictReader(open(file))
    data = []
    for row in csv:
        data.append(row)

    for trade in data:

        num_shares = float(trade["num_shares"])
        buy_price = float(trade["buy_price"])

        if not trade["sell_date"]:
            sell_date = None
        else:
            sell_date = datetime.strptime(trade["sell_date"], "%Y-%m-%d")

        if not trade["sell_price"]:
            sell_price = 0.0
        else:
            sell_price = float(trade["sell_price"])

        position_size = round(num_shares * buy_price, 2)
        net_pnl = round((num_shares * sell_price) - position_size, 2)
        net_roi = round(net_pnl / position_size * 100, 2)

        record = Trade(
            date=datetime.strptime(trade["date"], "%Y-%m-%d"),
            symbol=trade["symbol"].upper(),
            num_shares=num_shares,
            buy_price=buy_price,
            sell_date=sell_date,
            sell_price=sell_price,
            position_size=position_size,
            net_pnl=net_pnl,
            net_roi=net_roi,
            notes=trade["notes"],
        )

        db.session.add(record)
        db.session.commit()

    return


def checkdb():
    if len(Trade.query.all()) < 10:
        csv_import("sample_trades.csv")
