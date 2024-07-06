"""
This module starts the Flask app.
"""

from jim_bob.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
