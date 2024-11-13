import os
import warnings
from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from flask_smorest import Api, Blueprint, abort

class Base(DeclarativeBase):
    pass

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

def create_app():
    from tasks.models import Task
    from tasks.serializers import TaskSchema

    warnings.filterwarnings(
        "ignore",
        message="Multiple schemas resolved to the name "
    )
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['API_TITLE'] = 'My ECM API'
    app.config["API_VERSION"] = "1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/openapi"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    db.init_app(app)

    Migrate(app, db)
    api = Api(app)
    ma.init_app(app)

    from tasks.views import task_blueprint
    api.register_blueprint(task_blueprint)

    @app.route('/')
    def index():
        return '<h1>ECM Bonjour</h1>'

    @app.route('/user/<name>')
    def user(name):
        return render_template('user.html', name=name)

    return app