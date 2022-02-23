from app import app
from app.tools import create_db
from os import environ
from os.path import exists
import webbrowser
from waitress import serve


def main():
    # initialize database if it doesn't exist
    if not exists("./app/journal.db"):
        create_db()
        print("Database initialized")

    # auto-open the application
    # webbrowser.open("http://0.0.0.0:8080/")
    # port = int(environ.get("PORT", 8080))
    # serve(app, port=port)
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
