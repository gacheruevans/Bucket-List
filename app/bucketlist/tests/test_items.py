import json

import unittest

from flask import url_for

from app import db
from app.auth.models import Users
from app.bucketlist.models import Item
from app.test_config import globalTest


class Test_Items(globalTest):
    """
        something nice...
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

    def test_create_new_item(self):
        response = self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps(
                {
                    'name': 'Ziplining',
                    'done': False}),
            content_type='application/json',
            headers=self.token)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("created successfully",
                      data['message'])

    def test_can_view_all_items(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'test_item',
                'done': False
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('items'),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_view_a_item(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'test_item',
                'done': False,
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            url_for('oneitem', bucketlist_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_can_delete_item(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'test_item',
                'done': False
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.delete(
            url_for('oneitem', bucketlist_id=1),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

        response = self.client.get(
            url_for('oneitem', bucketlist_id=1),
            headers=self.token)
        self.assert_status(response, 400)

    def test_can_search_for_item(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'item1',
                'done': False,
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.get(
            '/api/v1/items?q=item',
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

        response = self.client.get(
            '/api/v1/items?q=none',
            headers=self.token)
        self.assert_status(response, 400)
        result = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(result)
        self.assertIn('does not match any bucketlist names',
                      result['message'])

    def test_can_edit_item(self):
        self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({
                'name': 'test_item',
                'done': False
            }),
            content_type='application/json',
            headers=self.token)
        response = self.client.put(
            url_for('oneitem', bucketlist_id=1),
            data=json.dumps({
                'name': 'Bangee jumping',
                'done': False
            }),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_create_existing_item(self):
        item = Item(
            name='Ziplining')

        db.session.add(item)
        db.session.commit()
        response = self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps(
                {
                    'name': 'Ziplining'}),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Item already exists",
                      data['message'])

    def test_incomplete_detail_on_item(self):
        response = self.client.post(
            url_for('items', bucketlist_id=1),
            data=json.dumps({'name': ''}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("provide a item",
                      data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
