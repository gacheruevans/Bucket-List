import datetime

import json

import unittest

from flask import url_for

from app import db
from app.test_config import globalTest


class TestBucketlist(globalTest):
    """
        This class holds the tests for creating new a new bucketlist, \
        view an bucketlist or bucketlists, edit bucketlists, delete \
        bucketlist and search for bucketlists.
    """

    def setUp(cls):
        db.create_all()
        cls.client.post(
            url_for('register'),
            data=json.dumps(
                {
                    'username': 'Evans',
                    'password': 'nd00th1ngz',
                    'email': 'gacheruevans0@gmail.com'})
        )
        response = cls.client.post(
            url_for('login'),
            data=json.dumps({
                'username': 'Evans',
                'password': 'nd00th1ngz'}),
        )
        data = json.loads(response.get_data(as_text=True))

        cls.token = {'Authorization': data['token']}

    def test_create_new_bucketlist(self):
        response = self.client.post(
            url_for('bucketlist'),
            data=json.dumps(
                {
                    'name': 'Adventure',
                    'date_created': str(datetime.datetime.now())}),
            headers=self.token)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("created bucketlist successfully",
                      data['message'])

    def test_view_all_bucketlists(self):
        self.client.post(
            url_for('bucketlist'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'date_created': str(datetime.datetime.now())
            }),
            headers=self.token)
        response = self.client.get(
            url_for('bucketlist'),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_view_a_bucketlists(self):
        self.client.post(
            url_for('bucketlist'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'date_created': str(datetime.datetime.now())
            }),
            headers=self.token)
        response = self.client.get(
            url_for('onebucketlist', bucketlists_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_delete_bucketlist(self):
        self.client.post(
            url_for('bucketlist'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'date_created': str(datetime.datetime.now())
            }),
            headers=self.token)
        response = self.client.delete(
            url_for('onebucketlist', bucketlists_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("successfully deleted",
                      data['message'])

        response = self.client.get(
            url_for('onebucketlist', bucketlists_id=1),
            headers=self.token)
        self.assert_status(response, 400)

    def test_search_for_bucketlist(self):
        self.client.post(
            url_for('bucketlist'),
            data=json.dumps({
                'name': 'bucketlist1',
                'date_created': str(datetime.datetime.now())
            }),
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
        self.assertIn('No bucketlist matching the search param',
                      result['message'])

    def test_edit_bucketlist(self):
        self.client.post(
            url_for('bucketlist'),
            data=json.dumps({
                'name': 'test_bucketlist',
                'date_created': str(datetime.datetime.now())
            }),
            headers=self.token)
        response = self.client.put(
            url_for('onebucketlist', bucketlists_id=1),
            data=json.dumps({
                'name': 'Travel',
                'date_created': str(datetime.datetime.now())
            }),
            headers=self.token)
        self.assert_200(response)

    def test_create_existing_bucketlist(self):
        self.client.post(
            url_for('bucketlist'),
            data=json.dumps(
                {
                    'name': 'Adventure'}),
            headers=self.token)

        response = self.client.post(
            url_for('bucketlist'),
            data=json.dumps(
                {
                    'name': 'Adventure'}),
            headers=self.token)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Bucketlist already exists",
                      data['message'])

    def test_incomplete_detail_on_bucketlist(self):
        response = self.client.post(
            url_for('bucketlist'),
            data=json.dumps({'name': ''}),
            headers=self.token)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Kindly provide the name",
                      data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
