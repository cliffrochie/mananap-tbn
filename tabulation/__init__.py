__version__ = '0.1.0'

from flask import Flask
#from tabulation.models.db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    # Routes
    from tabulation.routes.main_routes import main
    from tabulation.routes.generate_data.data_routes import data

    app = Flask(__name__)

    if not database_exists('mysql://root@localhost/tabulation'):
        create_database('mysql://root@localhost/tabulation')

    # Register routes
    app.register_blueprint(main, url_prefix='/api')
    app.register_blueprint(data, url_prefix='/api/data')

    CORS(app)
    cors = CORS(app, resources = {
        r'/*': {
            'origins': '*'
        }
    }, supports_credentials=True)

    app.config.from_object('tabulation.config')

    db.init_app(app)

    with app.test_request_context():
        db.create_all()

    return app