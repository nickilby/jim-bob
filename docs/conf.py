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

html_theme = "sphinx_rtd_theme"
html_sidebars = {
    "**": [
        "globaltoc.html",  # Main table of contents
        "sourcelink.html",  # Source link to GitHub
        "searchbox.html",  # Search box
    ]
}
