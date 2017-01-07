import json

import unittest

from flask import url_for

from app import db
from app.test_config import globalTest
from app.auth.models import Users


class testRegister(globalTest):

    def setUp(self):
        db.create_all()

    def test_register_endpoint(self):
        response = self.client.get(url_for('register'))
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertEqual('To register,send a POST request with username, \
            password and email to /auth/register.',
                         data['message'])

    def test_registration_new_user(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {
                    'username': 'Evans',
                    'password': 'nd00th1ngz',
                    'email': 'gacheruevans0@gmail.com'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("created successfully",
                      data['message'])

    def test_registration_existing_user(self):
        user = Users(
            username='Evans',
            password='nd00th1ngz',
            email='gacheruevans0@gmail.com')

        db.session.add(user)
        db.session.commit()

        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {
                    'username': 'Evans',
                    'password': 'nd00th1ngz',
                    'email': 'gacheruevans0@gmail.com'}),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("User already exists",
                      data['message'])

    def test_registration_with_short_password(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps({
                'username': 'Trial',
                'email': 'trial@gmail.com',
                'password': '123'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Password should be 4 or more characters",
                      data['message'])

    def test_incomplete_details_on_registration(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps({'username': 'Evans'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("provide a username, email and password",
                      data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
