"""_summary_

Returns:
    _type_: _description_
"""
import sqlite3

import click
from flask import current_app, g


def get_db():
    """_summary_

    Returns:
        _type_: _description_
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    """_summary_

    Args:
        e (_type_, optional): _description_. Defaults to None.
    """
    print(error)
    db_connexion = g.pop("db", None)

    if db_connexion is not None:
        db_connexion.close()


def init_db():
    """_summary_
    """
    db_connexion = get_db()

    with current_app.open_resource("schema.sql") as file:
        db_connexion.executescript(file.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """_summary_

    Args:
        app (_type_): _description_
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
