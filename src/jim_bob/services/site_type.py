from urllib.parse import urlparse

def determine_site_type(headers):
    """Determine site type from X-Origin-Server header."""
    x_origin_server = headers.get('X-Origin-Server', '')
    if x_origin_server.startswith('backend-coordinator'):
        return 'blocks'
    elif x_origin_server.startswith('z-'):
        return 'classic'
    return 'Unknown'

def construct_additional_urls(headers, site_type, original_url):
    """Construct additional URLs if site type is 'classic'."""
    if site_type == 'classic':
        x_host = headers.get('x-host', '')
        if 'live-' in x_host and '.cloud.contensis.com' in x_host:
            alias = x_host.split('live-')[1].split('.cloud.contensis.com')[0]
            print(f"Setting global_alias to: {alias}")  # Debug statement
            parsed_url = urlparse(original_url)
            path = parsed_url.path
            additional_urls = {
                'WEB1': f"https://z-{alias}-web1-live-{alias}.cloud.contensis.com{path}",
                'WEB2': f"https://z-{alias}-web2-live-{alias}.cloud.contensis.com{path}"
            }
            return additional_urls, alias
    return {}, None
