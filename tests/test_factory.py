""" Import """
from flaskr import create_app


def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    """_summary_

    Args:
        client (_type_): _description_
    """
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
