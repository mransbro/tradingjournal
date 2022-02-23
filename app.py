import csv
from app import app
from app.tools import create_db
from os.path import exists


def main():
    # initialize database if it doesn't exist
    if not exists("./app/journal.db"):
        create_db()
        print("Database initialized")

    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
