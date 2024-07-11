def determine_site_type(headers):
    """Determine site type from X-Origin-Server header."""
    x_origin_server = headers.get('X-Origin-Server', '')
    if x_origin_server.startswith('backend-coordinator'):
        return 'blocks'
    elif x_origin_server.startswith('z-'):
        return 'classic'
    return 'Unknown'
