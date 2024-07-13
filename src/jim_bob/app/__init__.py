"""
This module initializes the Flask app.
"""

from flask import Flask

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    from jim_bob.app.blueprints import routes  # pylint: disable=import-outside-toplevel
    app.register_blueprint(routes.main)

    return app
