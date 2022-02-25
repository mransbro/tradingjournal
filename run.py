from app import app
from app.tools import create_db, csv_import
from os.path import exists
from app.tools import csv_import
import logging


def main():
    # initialize database if it doesn't exist
    if not exists("./app/journal.db"):
        logging.debug("Databasse file not found. Creating a new db file.")
        create_db()
        csv_import()

    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
