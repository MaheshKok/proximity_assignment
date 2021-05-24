import pytest
from flask.app import Flask
from flask.testing import FlaskClient

from application import constants
from application import extensions as ext
from application.app import create_test_app


@pytest.fixture(scope="session", autouse=True)
def init_app():
    """
    Automatically create a Flask app instance.
    """
    constants.SQLALCHEMY_DATABASE_URI = f"{constants.SQLALCHEMY_DATABASE_URI }_test"
    return create_test_app()


@pytest.fixture(autouse=True)
def init_app_context(init_app):
    """Push a new app context for each test."""
    with init_app.app_context():
        yield


@pytest.fixture(scope="session", autouse=True)
def ensure_clean_database_start(init_app: Flask):
    """
    Ensure that the database always starts from a clean slate.

    It's possible that the test database we are connected to has lingering data.
    To eliminate this possibility, we ensure all tables have been dropped before
    the first test runs.
    """
    with init_app.app_context():
        ext.db.drop_all()


@pytest.fixture(scope="session", autouse=True)
def init_database(init_app):
    """Automatically create and then drop database tables."""
    with init_app.app_context():
        ext.db.create_all()
        yield
        ext.db.session.remove()
        ext.db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def clear_database():
    """Automatically truncate all database tables between tests runs."""
    yield
    ext.db.session.remove()
    for table in ext.db.engine.table_names():
        # very weired its unable to delete user table
        if table != "user":
            ext.db.session.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
    ext.db.session.commit()


@pytest.fixture()
def app(init_app: Flask) -> FlaskClient:
    """Access the Flask apps test_client"""
    return init_app.test_client()
