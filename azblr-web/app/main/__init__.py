from flask import Flask
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# from apscheduler.schedulers.background import BackgroundScheduler

from .config import Config
# from .crawler.score_crawler import crawl

db = MySQL()
flask_bcrypt = Bcrypt()
# sched = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_DATABASE_USER'] = Config.DATABASE_USER
    app.config['MYSQL_DATABASE_PASSWORD'] = Config.DATABASE_PASSWORD
    app.config['MYSQL_DATABASE_DB'] = Config.DATABASE_DB
    app.config['MYSQL_DATABASE_HOST'] = Config.DATABASE_HOST
    app.config['MYSQL_DATABASE_PORT'] = Config.DATABASE_PORT
    db.init_app(app)
    flask_bcrypt.init_app(app)
    # sched.start()
    CORS(app, resources = {
        r"/api/*": {"origin": "*"}
    })

    return app