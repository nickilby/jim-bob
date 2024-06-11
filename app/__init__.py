"""
This module initializes the Flask app.
"""

from flask import Flask

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    
    from app.routes import main
    app.register_blueprint(main)

    return app
