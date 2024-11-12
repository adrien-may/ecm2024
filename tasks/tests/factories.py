from app import db

import factory
from tests import common
from ..models import Task


class TaskFactory(factory.alchemy.SQLAlchemyModelFactory):
    title = factory.Faker("text")

    class Meta:
        model  = Task
        sqlalchemy_session = common.Session
