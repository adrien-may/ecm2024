from app import db
import json
from ..models import Task
from .factories import TaskFactory


def test_tasks_list(client, session):
    task = TaskFactory()
    session.commit()
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == task.title

def test_tasks_create(client, session):
    title = "my_test"
    # Ensure no task persist with this title
    Task.query.filter_by(title=title).delete()
    data = json.dumps({"title": "my_test"})
    response = client.post("/tasks/", data=data, content_type="application/json")
    assert response.status_code == 201
    response = client.post("/tasks/", data=data, content_type="application/json")
    assert response.status_code == 400

def test_tasks_get_one(client, session):
    task = TaskFactory()
    session.commit()
    task = Task.query.filter_by(title=task.title).first()
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    response = client.get(f"/tasks/{task.id + 1}")
    assert response.status_code == 404

def test_tasks_update_one(client, session):
    new_title = "new_title"
    # Ensure no task persist with this title
    session.query(Task).filter(Task.title == new_title).delete()
    task = TaskFactory()
    session.commit()
    task2 = session.query(Task).filter(Task.title == task.title).first()
    response = client.put(
        f"/tasks/{task2.id}",
        data=json.dumps({"title": new_title}),
        content_type="application/json",
    )
    assert response.status_code == 200
    response = client.put(
        f"/tasks/{task2.id + 10}",
        data=json.dumps({"title": new_title}),
        content_type="application/json",
    )
    assert response.status_code == 404
    session.query(Task).filter(Task.title == "already_existing").delete()
    session.commit()
    TaskFactory(title="already_existing")
    session.commit()
    task3 = session.query(Task).filter(Task.title == new_title).first()
    response = client.put(
        f"/tasks/{task3.id}",
        data=json.dumps({"title": "already_existing"}),
        content_type="application/json"
    )
    assert response.status_code == 400

def test_tasks_patch_one(app, client, session):
    new_title = "new_title"
    # Ensure no task persist with this title
    session.query(Task).filter(Task.title == new_title).delete()
    task = TaskFactory()
    session.commit()
    task2 = session.query(Task).filter(Task.title == task.title).first()
    response = client.patch(
        f"/tasks/{task2.id}",
        data=json.dumps({"done": True}),
        content_type="application/json",
    )
    assert response.status_code == 200
    response = client.patch(
        f"/tasks/{task2.id + 10}",
        data=json.dumps({"done": True}),
        content_type="application/json",
    )
    assert response.status_code == 404

def test_tasks_delete_one(client, session):
    task = TaskFactory()
    session.commit()
    task = Task.query.filter_by(title=task.title).first()
    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204
    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 404
