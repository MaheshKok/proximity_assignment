from flask import Flask

from application.blueprints.apis.views import register_json_routes
from application.extensions import register_extensions
from application.extensions.database import register_database


def _create_app():
    app = Flask(__name__)
    register_extensions(app)
    return app


def create_test_app() -> Flask:
    """Create a version of the application for unit testing"""
    app = _create_app()

    # app.config.update(TESTING=True, SERVER_NAME="localhost")
    register_json_routes(app)
    return app


def create_web_app():
    app = _create_app()
    register_database(app)
    register_json_routes(app)

    return app
