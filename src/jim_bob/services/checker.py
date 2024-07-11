import time
import requests
import ipaddress
from urllib.parse import urlparse
from .utils import add_schema_if_missing
from .ssl_details import get_ssl_certificate_details
from .dns_info import get_dns_info, ZENGENTI_IP_RANGE
from .site_type import determine_site_type, construct_additional_urls


def check_website(url):
    """Check the website status and DNS records."""
    url = add_schema_if_missing(url)
    result = {
        "status_message": "Red (Down)",
        "status_color": "red-status",
        "response_time": None,
        "content_length": None,
        "headers": {},
        "ssl_details": {},
        "redirects": [],
        "dns_info": {
            "ip": None,
            "cname": None,
            "ns_records": [],
            "status_color": "red-status",
            "is_zengenti": False
        },
        "site_type": "Unknown",
        "additional_urls": {},
        "alias": None
    }

    try:
        start_time = time.time()
        response = requests.get(url, headers={"debug": "true"}, allow_redirects=True)
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

        # DNS Lookup
        dns_info = get_dns_info(url)
        if dns_info["ip"]:
            dns_info["status_color"] = "green-status"
            if ipaddress.ip_address(dns_info["ip"]) in ZENGENTI_IP_RANGE:
                dns_info["is_zengenti"] = True

        result['dns_info'] = dns_info

        # Determine site type
        site_type = determine_site_type(headers)
        result['site_type'] = site_type

        # Construct additional URLs if site type is 'classic'
        additional_urls, alias = construct_additional_urls(headers, site_type, url)
        result['additional_urls'] = additional_urls
        result['alias'] = alias  # Store the alias in the result

        # Check status of additional URLs
        for name, additional_url in additional_urls.items():
            try:
                additional_response = requests.get(additional_url)
                print(f"{name} URL: {additional_url} - Status Code: {additional_response.status_code}")
                result['additional_urls'][name] = {
                    'url': additional_url,
                    'status_code': additional_response.status_code
                }
            except requests.RequestException as e:
                print(f"Failed to reach {name} URL: {additional_url} - Error: {e}")
                result['additional_urls'][name] = {
                    'url': additional_url,
                    'error': str(e)
                }

        # Log to terminal
        print(f"Initial URL: {url}")
        print(f"Final URL: {final_url}")
        print(f"Status Code: {final_status}")
        print(f"Response Time: {response_time:.2f} seconds")
        print(f"Content Length: {content_length} bytes")
        print(f"Headers: {headers}")
        print(f"SSL Details: {ssl_details}")
        print(f"Redirects: {redirects}")
        print(f"DNS Info: {dns_info}")
        print(f"Site Type: {result['site_type']}")  # Output site_type to terminal
        print(f"Additional URLs: {result['additional_urls']}")  # Output additional URLs to terminal
        print(f"Alias (from checker.py): {result['alias']}")  # Output alias to terminal

        status_message = (
            f"Green (200 OK) - Final URL: {final_url}"
            if final_status == 200 else
            f"Amber ({final_status}) - Final URL: {final_url}"
            if final_status in [301, 302] else
            f"Red ({final_status}) - Final URL: {final_url}"
        )

        status_color = (
            "green-status"
            if final_status == 200 else
            "amber-status"
            if final_status in [301, 302] else
            "red-status"
        )

        result.update({
            "status_message": status_message,
            "status_color": status_color,
            "response_time": response_time,
            "content_length": content_length,
            "headers": headers,
            "ssl_details": ssl_details,
            "redirects": redirects
        })

    except requests.exceptions.SSLError:
        result['dns_info'] = result.get('dns_info', {"status_color": "red-status", "is_zengenti": False})
        result.update({
            "status_message": "Amber (SSL Error)",
            "status_color": "amber-status"
        })
    except requests.exceptions.RequestException:
        result['dns_info'] = result.get('dns_info', {"status_color": "red-status", "is_zengenti": False})
        result.update({
            "status_message": "Red (Down)",
            "status_color": "red-status"
        })

    return result
