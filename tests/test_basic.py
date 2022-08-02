import unittest
import sys
from flask import session
sys.path.append('../beware')  # imports python file from parent directory
from beware import app  # imports flask app object


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    # test home page exists
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # test beware map page exists
    def test_beware_map(self):
        response = self.app.get('/bewaremap', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # test login page exists
    def test_login(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # test register page exists
    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # test profile page does not show when not logged in
    def test_profile(self):
        response = self.app.get('/myprofile', follow_redirects=True)
        self.assertNotIn(b"Your Reported Incidents", response.data)

    # test profile page shows when logged in
    def test_profile2(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = "test_name"
        response = self.app.get('/myprofile', follow_redirects=True)
        self.assertIn(b"Your Reported Incidents", response.data)

    # test report page does not show when not logged in
    def test_report(self):
        response = self.app.get('/report', follow_redirects=True)
        self.assertNotIn(b"NEW REPORT", response.data)

    # test report page shows when logged in
    def test_report2(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = "test_name"
        response = self.app.get('/report', follow_redirects=True)
        self.assertIn(b"NEW REPORT", response.data)


if __name__ == "__main__":
    unittest.main()
