from urllib.parse import urlparse


def add_schema_if_missing(url):
    """Add schema to URL if missing."""
    if not urlparse(url).scheme:
        return 'http://' + url
    return url
