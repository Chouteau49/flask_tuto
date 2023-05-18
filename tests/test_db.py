"""" Import """
import sqlite3

import pytest

from flaskr.db import get_db


def test_get_close_db(app):
    """_summary_

    Args:
        app (_type_): _description_
    """
    with app.app_context():
        db_connexion = get_db()
        assert db_connexion is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as error:
        db_connexion.execute("SELECT 1")

    assert "closed" in str(error.value)


def test_init_db_command(runner, monkeypatch):
    """_summary_

    Args:
        runner (_type_): _description_
        monkeypatch (_type_): _description_
    """

    class Recorder:
        """_summary_"""

        called = False

    def fake_init_db():
        """_summary_"""
        Recorder.called = True

    monkeypatch.setattr("flaskr.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
