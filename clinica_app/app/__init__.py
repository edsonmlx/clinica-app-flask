import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

with app.app_context():
    from app.index_view import ClinicaIndexView
    appbuilder = AppBuilder(app, db.session, indexview=ClinicaIndexView)
    from app import views