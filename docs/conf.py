"""Configuration for Sphinx documentation using the Read the Docs theme."""

# Project information
project = "Jim Bob"
author = "Nic Kilby"
release = "1"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",  # To include source code links
    "sphinxcontrib.mermaid",
]
html_static_path = ['_static']
html_theme = "sphinx_rtd_theme"
html_sidebars = {
    "**": [
        "globaltoc.html",  # Main table of contents
        "sourcelink.html",  # Source link to GitHub
        "searchbox.html",  # Search box
    ]
}

def setup(app):
    """Set up so that we can add custom features."""
    app.add_css_file('custom.css')

