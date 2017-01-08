import datetime

import json

import unittest

from flask import url_for

from app import db
from app.auth.models import Users
from app.bucketlist.models import Bucketlist
from app.test_config import globalTest


class TestBucketlist(globalTest):
    """
        This class holds all the test methods that...
    """

    def setUp(cls):
        db.create_all()
        response = cls.client.post(
            url_for('login'),
            data=json.dumps({
                'username': 'Evans',
                'password': 'nd00th1ngz'}),
            content_type="application/json")
        data = json.loads(response.get_data(as_text=True))
        cls.token = {'Authorization': data['token']}
        cls.logged_in_user = Users.query.filter_by(username='Evans').first()

    def test_create_new_bucketlist(self):
        response = self.client.post(
            url_for('bucketlist'),
            data=json.dumps(
                {
                    'name': 'Adventure',
                    'date_created': str(datetime.datetime.now()),
                    'created_by': 'self.logged_in_user.username'}),
            content_type='application/json',
            headers=self.token)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("created successfully",
                      data['message'])

    def test_can_view_all_bucketlists(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'date_created': str(datetime.datetime.now()),
                'created_by': self.logged_in_user.username
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('bucketlists'),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_view_a_bucketlists(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'date_created': str(datetime.datetime.now()),
                'created_by': self.logged_in_user.username
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('one_bucketlist', bucketlist_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_delete_bucketlist(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'date_created': str(datetime.datetime.now()),
                'created_by': self.logged_in_user.username
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.delete(
            url_for('one_bucketlist', bucketlist_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

        response = self.client.get(
            url_for('one_bucketlist', bucketlist_id=1),
            headers=self.token)
        self.assert_status(response, 400)

    def test_can_search_for_bucketlist(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'bucketlist1',
                'date_created': str(datetime.datetime.now()),
                'created_by': self.logged_in_user.username
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            '/api/v1/bucketlists?q=bucketlist',
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

        response = self.client.get(
            '/api/v1/bucketlists?q=none',
            headers=self.token)
        self.assert_status(response, 400)
        result = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(result)
        self.assertIn('does not match any bucketlist names',
                      result['message'])

    def test_can_edit_bucketlist(self):
        self.client.post(
            url_for('bucketlists'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'date_created': str(datetime.datetime.now()),
                'created_by': self.logged_in_user.username
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.put(
            url_for('one_bucketlist', bucketlist_id=1),
            data=json.dumps({
                'name': 'Travel',
                'date_created': str(datetime.datetime.now()),
                'created_by': self.logged_in_user.username
            }),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_create_existing_bucketlist(self):
        bucketlist = Bucketlist(
            name='Adventure')

        db.session.add(bucketlist)
        db.session.commit()
        response = self.client.post(
            url_for('bucketlist'),
            data=json.dumps(
                {
                    'name': 'Adventure'}),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Bucketlist already exists",
                      data['message'])

    def test_incomplete_detail_on_bucketlist(self):
        response = self.client.post(
            url_for('bucketlist'),
            data=json.dumps({'name': ''}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("provide a name",
                      data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
