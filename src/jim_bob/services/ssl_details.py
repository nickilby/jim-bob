import ssl
import socket
from urllib.parse import urlparse

def get_ssl_certificate_details(url):
    """Retrieve SSL certificate details."""
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
