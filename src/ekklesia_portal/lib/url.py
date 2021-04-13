from urllib.parse import urlencode, urlparse, parse_qs


def url_change_query(url, **query_vars):
    """Add or update variables in the query string of the given URL"""
    parsed_url = urlparse(url)
    query = urlencode({**parse_qs(parsed_url.query), **query_vars}, doseq=True)
    return parsed_url._replace(query=query).geturl()
