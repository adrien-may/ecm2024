from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Task

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
