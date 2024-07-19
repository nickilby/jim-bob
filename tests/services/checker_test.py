"""Tests for the checker."""

from jim_bob.app.services import checker

def test_add_schema_if_missing():
    """Confirm that the schema gets added."""
    # ARRANGE
    url_without_schema = "www.google.com"
    # ACT
    url_with_schema  = checker.add_schema_if_missing(url_without_schema )
    # ASSERT
    assert url_with_schema.startswith("http")
