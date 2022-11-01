# Trading journal

A simple trade journal app built with Python Flask.

![home](https://github.com/mransbro/tradingjournal/blob/main/img/homepage.png)

## Installation

Make sure you have the following prereqs:

1. Python >= 3.10
2. Pip
3. Git

Installing the app is easy:

1. Clone the repository in the directory you wish: `git clone` https://github.com/mransbro/tradingjournal.git
2. Enter the tradingjournal directory. (cd tradingjournal)
3. Install requirements: `pip install -r requirements.txt`
4. Run the app: `python3 run.py`.
5. For production use gunicron `gunicorn -w 4 "app:init_app()"`

## Want to try it out

Demo running on [Render](https://tradingjounral.onrender.com)

## Roadmap

- Error handling
- Tests
- Reduce number of packages

# Built with

- [Python 3](https://python.org): programming language
- [Flask](https://flask.palletsprojects.com): web framework
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com): database
- [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/): python WSGI server
- [Bootstrap](https://getbootstrap.com/): CSS and JS framework
- [Black](https://black.readthedocs.io/en/stable/): Python linting
