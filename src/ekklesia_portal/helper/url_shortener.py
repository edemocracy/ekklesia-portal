from __future__ import with_statement

import contextlib
from urllib.parse import urlencode
from urllib.request import urlopen


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')
