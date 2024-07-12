"""This module defines the routes for the Flask app."""

from flask import Blueprint, render_template, request, redirect, url_for
from jim_bob.services.checker import check_website

main = Blueprint('main', __name__)

# Global list to store past 10 unique URLs
past_tests = []

@main.route("/", methods=["GET", "POST"])
def index():
    """
    Handle the main route to display the diagnostics form and results.
    """
    status_message = None
    status_color = ""
    url = request.args.get('url', '')

    additional_info = {}
    site_type = "Unknown"
    if request.method == "POST":
        url = request.form.get("url")
        if url and url not in past_tests:
            past_tests.append(url)
            if len(past_tests) > 10:
                past_tests.pop(0)
        return redirect(url_for('main.index', url=url))

    if url:
        result = check_website(url)
        status_message = result.get("status_message")
        status_color = result.get("status_color")
        additional_info = result
        site_type = result.get("site_type", "Unknown")
        print(f"Site Type: {site_type}")  # Output site_type to terminal

    print(f"Rendering template with site_type: {site_type}")  # Debug print to confirm value passed to template

    return render_template(
        "index.html",
        status_message=status_message,
        status_color=status_color,
        past_tests=past_tests,
        current_url=url,
        additional_info=additional_info,
        site_type=site_type
    )
