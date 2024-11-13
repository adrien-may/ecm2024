from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app import db
from .models import Task
from .serializers import TaskSchema
from sqlalchemy.orm.exc import NoResultFound

task_blueprint = Blueprint(
    "tasks", "tasks", url_prefix="/tasks", description="Operations on tasks"
)

@task_blueprint.route("/")
class Tasks(MethodView):
    @task_blueprint.response(200, TaskSchema(many=True))
    def get(self):
        return db.session.query(Task).all()

    @task_blueprint.arguments(TaskSchema(only=["title"]))
    @task_blueprint.response(201, TaskSchema)
    def post(self, new_data):
        try:
            task = Task(**new_data)
            db.session.add(task)
            db.session.commit()
            return task
        except Exception as e:
            abort(400, message="An error occurred")


@task_blueprint.route("/<int:task_id>")
class TasksById(MethodView):
    @task_blueprint.response(200, TaskSchema)
    def get(self, task_id):
        try:
            return db.session.get_one(Task, task_id)
        except NoResultFound:
            abort(404, message="Task not found")

    @task_blueprint.arguments(TaskSchema(only=["title"]))
    @task_blueprint.response(200, TaskSchema)
    def put(self, update_data, task_id):
        try:
            task = db.session.get_one(Task, task_id)
        except NoResultFound:
            abort(404, message="Task not found")

        try:
            task.title = update_data["title"]
            db.session.add(task)
            db.session.commit()
        except Exception as e:
            abort(400, message="An error occurred")
        return task

    @task_blueprint.arguments(TaskSchema(only=["done"]))
    @task_blueprint.response(200, TaskSchema)
    def patch(self, update_data, task_id):
        """Update existing task"""
        try:
            task = db.session.get_one(Task, task_id)
        except NoResultFound:
            abort(404, message="Task not found")
        task.done = update_data["done"]
        db.session.add(task)
        db.session.commit()
        return task


    @task_blueprint.response(204)
    def delete(self, task_id):
        """Delete task"""
        try:
            task = db.session.get_one(Task, task_id)
            db.session.delete(task)
            db.session.commit()
        except NoResultFound:
            abort(404, message="Task not found")
