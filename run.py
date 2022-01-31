from app import app
from app.app import create_db
import os
import webbrowser
from waitress import serve


def main():
    # initialize database if it doesn't exist
    current_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(current_path, "journal.db")):
        create_db()
        print("Database initialized")

    # auto-open the application
    webbrowser.open("http://0.0.0.0:8080/")
    serve(app, port=8080)


if __name__ == "__main__":
    main()
