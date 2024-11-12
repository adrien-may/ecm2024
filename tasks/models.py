import datetime

from app import db

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Task(db.Model):
    __tablename__ = 'Task'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    creation_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    done: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return self.title
