import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow

class Base(DeclarativeBase):
    pass

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from tasks.models import Task
    from tasks.serializers import TaskSchema

    Migrate(app, db)

    @app.route('/')
    def index():
        return '<h1>ECM Bonjour</h1>'


    @app.route('/user/<name>')
    def user(name):
        return render_template('user.html', name=name)

    @app.route('/todoz')
    def my_better_api_route():
        tasks = Task.query.all()
        return {"results": TaskSchema(many=True).dump(tasks)}


    return app