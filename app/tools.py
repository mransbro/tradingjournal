from . import db

allowed_extensions = {"csv"}


# initialize database
def create_db():
    db.create_all()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
