from datetime import datetime
from .shibboleth_login import ShibbolethClient
from .parser import REGISTERED_PARSERS, get_key_from_url, GeneralParser
from .page import Page


class PortalBrowser(object):
    """Wrapper class for crawling Portal website"""

    def __init__(self, username: str, password: str):
        """
        Init instance
        :param username: your student id such as 'b0000000'
        :param password: password for your student id
        """
        self._username = username
        self._password = password
        self._client = ShibbolethClient(self._username, self._password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()

    def get_page(self, url: str, **kwards) -> Page:
        """
        Get `Page` object by url.
        :param url: str
        :param kwards: option for `requests.Session.get`
        :return: `Page` object
        """
        key = get_key_from_url(url)
        if key not in REGISTERED_PARSERS:
            parser = GeneralParser
        else:
            parser = REGISTERED_PARSERS[key]
        resp = self._client.get(url, **kwards)
        return Page(response=resp, parser=parser, access_at=datetime.now())