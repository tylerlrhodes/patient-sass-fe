from flask import Flask

from model import db
import config
import logging
import time

log = logging.getLogger(__name__)
MAX_CONNECT_TRIES = 3
SLEEP_TIME = 1

def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    # in case DB is temporarily down
    for i in range(0, MAX_CONNECT_TRIES + 1):
      try:
        db.create_all()
        break
      except:
        log.exception('Creating db connection')
        if i == MAX_CONNECT_TRIES:
          raise Exception("Could not connect to the database after {} tries".format(i))
        time.sleep(SLEEP_TIME)

    return flask_app
