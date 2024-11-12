from flask import Flask

from app import app


def test_app():
    assert app is not None
    assert isinstance(app, Flask)
