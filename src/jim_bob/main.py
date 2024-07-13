"""
This module starts the Flask app.
"""
import flask
from jim_bob.app.blueprints import routes
import os

def create_app():
    """Create and configure the Flask app."""
    the_app = flask.Flask(__name__, template_folder='app/templates')
    the_app.config['SECRET_KEY'] = os.urandom(24)
    the_app.register_blueprint(routes.main)
    return the_app


def main():
    app = create_app()
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
