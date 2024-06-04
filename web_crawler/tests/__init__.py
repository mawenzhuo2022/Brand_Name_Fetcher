# -*- coding: utf-8 -*-
# @Author  : Wenzhuo Ma
# @Time    : 2024/5/27 11:14
# @Function:
import unittest
import requests_mock
from src.website_fetcher import get_brand_names_from_wikipedia

class TestWebsiteFetcher(unittest.TestCase):
    @requests_mock.Mocker()
    def get_brand_names_from_existing_page(self, m):
        m.get('https://en.wikipedia.org/wiki/Cisco_Systems', text='<a class="interlanguage-link-target" hreflang="fr" href="https://fr.wikipedia.org/wiki/Cisco_Systems">Français</a>')
        result = get_brand_names_from_wikipedia('https://en.wikipedia.org/wiki/Cisco_Systems')
        self.assertEqual(result, {'fr': 'Français'})

    @requests_mock.Mocker()
    def get_brand_names_from_non_existing_page(self, m):
        m.get('https://en.wikipedia.org/wiki/NonExistingPage', status_code=404)
        result = get_brand_names_from_wikipedia('https://en.wikipedia.org/wiki/NonExistingPage')
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def get_brand_names_from_page_without_interlanguage_links(self, m):
        m.get('https://en.wikipedia.org/wiki/PageWithoutInterlanguageLinks', text='<a class="other-link" hreflang="fr" href="https://fr.wikipedia.org/wiki/PageWithoutInterlanguageLinks">Français</a>')
        result = get_brand_names_from_wikipedia('https://en.wikipedia.org/wiki/PageWithoutInterlanguageLinks')
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
