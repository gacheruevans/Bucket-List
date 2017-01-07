import json

import unittest

from flask import url_for

from app import db
from app.test_config import globalTest
from app.auth.models import Users


class testLogin(globalTest):
    """
        This class has the setUp method that creates a new user.
        Has a test index endpoint which checks for successful indexpage load.
        Has a test login endpoint which checks for successful post.
        Has a test login with correct cerdentials which checks for successful login.
        Has a test login with non existent user.
        Has a test login with empty username or email.
        Has a tear down method that closes all sessions.
    """

    def setUp(self):
        db.create_all()
        user = Users(
            username='Evans',
            email='gacheruevans0@gmail.com',
            password='nd00th1ngz')
        db.session.add(user)
        db.session.commit()

    def test_index_endpoint(self):
        response = self.client.get(url_for('home'))
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertIn('Welcome to the BucketList API.',
                      data['message'])

    def test_login_endpoint(self):
        response = self.client.get(url_for('login'))
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertEqual('To login,send a POST request to /auth/login.',
                         data['message'])

    def test_login_with_right_credentials(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': 'Evans',
                 'password': 'nd00th1ngz'}),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("token", data.keys())

    def test_login_with_non_existing_user(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': 'Ann',
                 'password': 'm0nty'}),
            content_type='application/json')
        self.assert_status(response, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("User does not exist", data['message'])

    def test_login_with_empty_username_or_password(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {
                    'username': '',
                    'password': ''}),
            content_type='application/json')
        self.assert_status(response, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertEqual('Kindly fill in the missing details',
                         data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
