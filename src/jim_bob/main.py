"""
This module starts the Flask app.
"""
import flask
from jim_bob.app.blueprints import home

def create_app():
    """Create and configure the Flask app."""
    app = flask.Flask(__name__)

     # pylint: disable=import-outside-toplevel
    app.register_blueprint(main)
    app.register_blueprint(home.routes)

    return app

def main() -> None:
    app = create_app()
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
