from flask import Flask
from flask_restx import Api
from .utils import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .auth.authuser import auth_namespace
from .links.linkaction import link_namespace

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mono29000eb@passsecret'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdatabase.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    JWTManager(app)
    Migrate(app, db)
    api = Api(app, title="Violet Api Class")
    api.add_namespace(auth_namespace, path='/api/auth')
    api.add_namespace(link_namespace, path='/api/link')
    
    return app