import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, UnprocessableEntity
from .notify import NotifyExtension
from . import __version__
from .db import db, register_db_cli

try:
    from flask_cors import CORS
except ImportError:
    CORS = None


def create_app():
    from .server import api

    app = Flask(__name__)
    if os.environ.get("FLASK_ENABLE_CORS") and CORS is not None:
        CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    register_error_handlers(app)
    db.init_app(app)
    register_db_cli(app)
    NotifyExtension(app, os.environ.get('NOTIFY_URL'), os.environ.get('NOTIFY_TOKEN'))
    app.register_blueprint(api)
    return app


def register_spec(test=False, test_host="localhost", test_port=12345):
    servers = (
        [{"url": f"http://{test_host}:{test_port}", "description": "Test server"}]
        if test
        else []
    )

    # Create an APISpec
    spec = APISpec(
        title="OpenReferee",
        version=__version__,
        openapi_version="3.0.2",
        info={
            "contact": {
                "name": "Indico Team",
                "url": "https://github.com/indico/openreferee",
                "email": "indico-team@cern.ch",
            }
        },
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        servers=servers,
        tags=[
            {"name": t} for t in ("create", "event", "get", "info", "remove", "service")
        ],
    )
    spec.components.security_scheme(
        "bearer_token", {"type": "http", "scheme": "bearer"}
    )
    return spec


def register_error_handlers(app):
    @app.errorhandler(UnprocessableEntity)
    def handle_unprocessableentity(exc):
        data = getattr(exc, "data", None)
        if data and "messages" in data:
            # this error came from a webargs parsing failure
            response = jsonify(webargs_errors=data["messages"])
            response.status_code = exc.code
            return response
        if exc.response:
            return exc
        return "Unprocessable Entity"

    @app.errorhandler(HTTPException)
    def _handle_http_exception(exc):
        return jsonify(error=exc.description), exc.code

    @app.errorhandler(Exception)
    def _handle_exception(exc):
        app.logger.exception("Request failed")
        return jsonify(error="Internal error"), 500
