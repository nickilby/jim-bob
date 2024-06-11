import os

"""
This module contains the configuration settings for the Flask app.
"""

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = True
