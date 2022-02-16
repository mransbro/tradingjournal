from . import db
from datetime import datetime

dateformat = "%Y-%m-%d"


class DailyRoutine(db.Model):
    __tablename__ = "dailyroutine"
    date = db.Column(db.Date, primary_key=True)
    stocks_above_20ma = db.Column(db.Integer, unique=False, nullable=True)
    stocks_above_50ma = db.Column(db.Integer, unique=False, nullable=True)
    stocks_above_200ma = db.Column(db.Integer, unique=False, nullable=True)

    def to_dict(self):
        return {
            "date": self.date.strftime(dateformat),
            "stocks_above_20ma": self.stocks_above_20ma,
            "stocks_above_50ma": self.stocks_above_50ma,
            "stocks_above_200ma": self.stocks_above_200ma,
        }


class WeeklyRoutine(db.Model):
    __tablename__ = "weeklyroutine"
    date = db.Column(db.Date, primary_key=True)
    industry_groups = db.Column(db.String, nullable=True)
    scans = db.Column(db.Boolean, default=False, server_default="False")
    watchlist = db.Column(db.Boolean, default=False, server_default="False")
    focuslist = db.Column(db.Boolean, default=False, server_default="False")
    open_positions = db.Column(db.Boolean, default=False, server_default="False")

    def to_dict(self):
        return {
            "date": self.date.strftime(dateformat),
            "industry_groups": self.industry_groups,
            "scans": self.scans,
            "watchlist": self.watchlist,
            "focuslist": self.focuslist,
            "open_positions": self.open_positions,
        }


class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    symbol = db.Column(db.String, nullable=False)
    position_size = db.Column(db.Integer, nullable=False)
    net_pnl = db.Column(db.Integer, default=0)
    net_roi = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime(dateformat),
            "symbol": self.symbol,
            "position_size": self.position_size,
            "net_pnl": self.net_pnl,
            "net_roi": self.net_roi,
            "notes": self.notes,
        }
