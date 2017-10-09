import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from ext import login_manager

from views import *

from models import db
from models import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = 'root:root@127.0.0.1/superhero'

DATABASE_URL = '{protocol}{path}'.format(
    protocol='mysql://',
    path=DATA_FILE
)


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()


def application():
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        DEBUG=True,
        SQLALCHEMY_DATABASE_URI=DATABASE_URL,
        SECRET_KEY=r"\x046=\x11\xb6\xb9)\x1d\xd3\xdaS{\xca\x1e'\xefPm\xf5Y8"
    )

    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/bhul_bhulai_ya/<page>', 'bhul_bhulai_ya', bhul_bhulai_ya,
                     methods=['GET', 'POST'])
    app.add_url_rule('/bhul_bhulai_ya', 'bhul_bhulai_ya', bhul_bhulai_ya,
                     methods=['GET', 'POST'])
    app.add_url_rule('/dashboard', 'dashboard', dashboard, methods=['GET', 'POST'])
    app.add_url_rule('/download/<member_id>/<subscription_id>', 'download', download, methods=['GET', 'POST'])
    app.add_url_rule('/lab', 'lab', lab, methods=['POST'])

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    return app


application = application()


if __name__ == '__main__':
    application.run(host='0.0.0.0')
