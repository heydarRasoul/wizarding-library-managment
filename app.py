from flask import Flask, jsonify, request

import os 

from db import *
import routes

from models.book import Books
from models.school import Schools
from models.spell import Spells
from models.wizard import Wizards
from models.wizard_specializations import WizardSpecialization

flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_PORT")

database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port =os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_scheme}{database_user}@{database_address}:{database_port}/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)

app.register_blueprint(routes.book)
app.register_blueprint(routes.school)
app.register_blueprint(routes.spell)
app.register_blueprint(routes.wizard)
app.register_blueprint(routes.wizard_specialization)


def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully")

if __name__ == '__main__':
    create_tables()
    app.run(host=flask_host, port=flask_port)

