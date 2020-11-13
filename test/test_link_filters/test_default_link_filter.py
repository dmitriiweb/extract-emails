import unittest

from extract_emails.link_filters import DefaultLinkFilter, ContactInfoLinkFilter


class TestDefaultLinkFilter(unittest.TestCase):
    def test_filter(self):
        urls = ['https://example.com', '/page1.html', 'page2.html', 'https://example2.com', 'page1.html']
        website = 'https://example.com'
        f = DefaultLinkFilter(website)
        res = ['https://example.com', 'https://example.com/page1.html', 'https://example.com/page2.html']
        self.assertEqual(f.filter(urls), res)

    def test_get_website_address(self):
        url = 'https://example.com/page.html?param=123&param2=321'
        self.assertEqual(DefaultLinkFilter.get_website_address(url), 'https://example.com/')

class TestContactInfoLinkFilter(unittest.TestCase):
    def test_filter(self):
        urls = ['https://example.com', '/page1.html', 'page2.html', 'https://example2.com', 'page1.html',
            'https://example.com/about', 'https://example.com/contact']
        website = 'https://example.com'
        f = ContactInfoLinkFilter(website, use_default=False)
        res = ['https://example.com/about', 'https://example.com/contact']
        self.assertEqual(f.filter(urls), res)

    def test_get_website_address(self):
        url = 'https://example.com/page.html?param=123&param2=321'
        self.assertEqual(ContactInfoLinkFilter.get_website_address(url), 'https://example.com/')