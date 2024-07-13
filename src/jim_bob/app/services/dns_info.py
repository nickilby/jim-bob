import contextlib
import ipaddress
import socket
from urllib.parse import urlparse

import dns.resolver

ZENGENTI_IP_RANGE = ipaddress.ip_network("185.18.136.0/22")


def get_dns_info(url):
    """Retrieve DNS information including IP, CNAME, and NS records."""
    hostname = urlparse(url).hostname
    dns_info = {
        "ip": None,
        "cname": None,
        "ns_records": [],
        "status_color": "red-status",
        "is_zengenti": False,
    }
    with contextlib.suppress(
        socket.gaierror,
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.resolver.NoNameservers,
    ):
        dns_info["ip"] = socket.gethostbyname(hostname)
        if cname_records := dns.resolver.resolve(hostname, "CNAME"):
            dns_info["cname"] = str(cname_records[0].target)
        ns_records = dns.resolver.resolve(hostname, "NS")
        for ns_record in ns_records:
            dns_info["ns_records"].append(str(ns_record.target))
        if dns_info["ip"]:
            dns_info["status_color"] = "green-status"
            if ipaddress.ip_address(dns_info["ip"]) in ZENGENTI_IP_RANGE:
                dns_info["is_zengenti"] = True
    return dns_info
