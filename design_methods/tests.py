"""
Tests for basic features such as the pages, Users, etc.
"""
import unittest
import xml.dom.minidom as minidom
from django.test import TestCase
from django.contrib.auth.models import User

"""
A utility class with some custom methods to make testing easier
"""

class EasyTests(TestCase):
    fixtures = ['test_data.json', 'users']
    """
    Common set-up procedures
    """
    def setUp(self):
        # nothing for now
        return

    """
    Basic check to see if the url has a good response
    """
    def responds_to(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    """
    Check to see if a page contains a given string
    """
    def has_text(self, url, text):
        response = self.client.get(url)
        self.assertContains(response, text)

    """
    Get the contents of a given tag at the url as an array of strings
    """
    def get_contents_of(self, url, tag):
        contents = []
        response = self.client.get(url)
        nodeList = minidom.parseString(response.content).getElementsByTagName(tag)
        for node in nodeList:
            for text in node.childNodes:
                contents.append(text.data)
        return contents

    """
    Check to see if a tag in the url contains the given text
    """
    def tag_has_contents(self, url, tag, text):
        contents = self.get_contents_of(url, tag)
        for content in contents:
            self.assertIn(text, content)

class HomePageTests(EasyTests):
    """
    Since this test is for one specific URI, set it as a field
    """
    def setUp(self):
        EasyTests.setUp(self)
        self.url = '/'

    """
    Simple tests to make sure there are no weird errors.
    Also to test helper methods
    """
    def test_sanity(self):
        self.responds_to(self.url)
        self.has_text(self.url, 'Welcome')
        self.tag_has_contents(self.url, 'h1', 'Design')

    """
    Test to see that the home page changes after login
    """
    def test_login(self):
        self.tag_has_contents(self.url, 'h1', 'Design')
        self.assertTrue(self.client.login(username='keien', password='foobar'))
        self.tag_has_contents(self.url, 'h1', 'keien')

    def runTest(self):
        self.test_sanity()
        self.test_login()

class UserTests(EasyTests):
    """
    Retrieve a user for testing
    """
    def setUp(self):
        self.user = User.objects.get(username='keien')

    """
    Test basic model functionalities
    """
    def test_sanity(self):
        self.assertEqual(self.user.username, "keien")
        self.assertEqual(self.user.email, "keienohta@gmail.com")

    def runTest(self):
        self.test_sanity()

"""
Set up test suite
"""
def suite():
    suite = unittest.TestSuite()

    suite.addTest(HomePageTests())
    suite.addTest(UserTests())

    return suite

