"""_summary_

Returns:
    _type_: _description_

Yields:
    _type_: _description_
"""
import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db
from flaskr.db import init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    """_summary_"""

    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        """_summary_

        Args:
            username (str, optional): _description_. Defaults to "test".
            password (str, optional): _description_. Defaults to "test".

        Returns:
            _type_: _description_
        """
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """_summary_

    Args:
        client (_type_): _description_

    Returns:
        _type_: _description_
    """
    return AuthActions(client)
