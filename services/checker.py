import requests
from urllib.parse import urlparse
import time
import socket
import ssl
from datetime import datetime

def add_schema_if_missing(url):
    if not urlparse(url).scheme:
        return 'http://' + url
    return url

def check_website(url):
    url = add_schema_if_missing(url)
    result = {
        "status_message": "Red (Down)",
        "status_color": "w3-pale-red w3-border-red",
        "response_time": None,
        "content_length": None,
        "headers": {},
        "ssl_details": {},
        "redirects": []
    }

    try:
        start_time = time.time()
        response = requests.get(url, allow_redirects=True)
        response_time = time.time() - start_time

        # Capture redirect history
        redirects = [(r.status_code, r.url) for r in response.history]

        # Final URL after following redirects
        final_url = response.url
        final_status = response.status_code
        headers = response.headers
        content_length = len(response.content)
        
        # SSL Certificate Details
        ssl_details = {}
        if urlparse(final_url).scheme == 'https':
            ssl_details = get_ssl_certificate_details(final_url)

        # Log to terminal
        print(f"Initial URL: {url}")
        print(f"Final URL: {final_url}")
        print(f"Status Code: {final_status}")
        print(f"Response Time: {response_time:.2f} seconds")
        print(f"Content Length: {content_length} bytes")
        print(f"Headers: {headers}")
        print(f"SSL Details: {ssl_details}")
        print(f"Redirects: {redirects}")

        result.update({
            "status_message": f"Green (200 OK) - Final URL: {final_url}" if final_status == 200 else f"Amber ({final_status}) - Final URL: {final_url}" if final_status in [301, 302] else f"Red ({final_status}) - Final URL: {final_url}",
            "status_color": "w3-pale-green w3-border-green" if final_status == 200 else "w3-pale-yellow w3-border-yellow" if final_status in [301, 302] else "w3-pale-red w3-border-red",
            "response_time": response_time,
            "content_length": content_length,
            "headers": headers,
            "ssl_details": ssl_details,
            "redirects": redirects
        })

    except requests.exceptions.SSLError:
        result.update({
            "status_message": "Amber (SSL Error)",
            "status_color": "w3-pale-yellow w3-border-yellow"
        })
    except requests.exceptions.RequestException:
        result.update({
            "status_message": "Red (Down)",
            "status_color": "w3-pale-red w3-border-red"
        })
    
    return result

def get_ssl_certificate_details(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

            return {
                "issuer": dict(x[0] for x in cert['issuer']),
                "notBefore": cert['notBefore'],
                "notAfter": cert['notAfter'],
                "subject": dict(x[0] for x in cert['subject'])
            }
