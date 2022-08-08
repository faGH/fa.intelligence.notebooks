'''This module defines HTML data access components.'''
import requests
from bs4 import BeautifulSoup

class HtmlDataAccess:
    '''HTML-related functionality.'''

    def get_page(self, url: str) -> object:
        '''Get a queryable HTML page via a URL.'''

        response: requests.Response = requests.get(url=url, headers={
            'User-Agent': 'PostmanRuntime/7.29.0'
        })
        response_text: str = response.text

        return BeautifulSoup(response_text, 'html.parser')
