from .factories import TaskFactory


def test_task_repr(session):
    task = TaskFactory()
    session.commit()
    assert repr(task) == task.title
