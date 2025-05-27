from flask import Flask
from .models import db
from .routes import api
from .config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    app.register_blueprint(api, url_prefix='/api')
    return app