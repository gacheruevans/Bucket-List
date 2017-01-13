import json
import datetime
import unittest

from flask import url_for

from app import db
from app.auth.models import Users
from app.bucketlist.models import Bucketlist, Item
from app.test_config import globalTest


class Test_Items(globalTest):
    """
        This class holds the tests for creating new a new item, \
        view an item or items, edit items, delete item and search \
        items for their respective bucketlists.
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

        cls.client.post(
            url_for('bucketlist'),
            data=json.dumps(
                {
                    'name': 'Adventure',
                    'date_created': str(datetime.datetime.now())}),
            headers=cls.token)
        cls.bucketlist = Bucketlist.query.filter_by(name="Adventure").first()

    def test_create_new_item(self):
        response = self.client.post(
            url_for('items', bucketlists_id=self.bucketlist.id),
            data=json.dumps(
                {
                    'name': 'Ziplining'
                }),
            headers=self.token)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("created bucketlist item successfully",
                      data['message'])

    def test_view_all_items(self):
        self.client.post(
            url_for('items', bucketlists_id=self.bucketlist.id),
            data=json.dumps({
                'name': 'test_item',
                'done': False
            }),
            headers=self.token)
        response = self.client.get(
            url_for('items', bucketlists_id=self.bucketlist.id),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_view_an_item(self):
        self.client.post(
            url_for('items', bucketlists_id=self.bucketlist.id),
            data=json.dumps({
                'name': 'test_item',
                'done': False,
            }),
            headers=self.token)
        item = Item.query.filter_by(name="test_item").first()
        response = self.client.get(
            url_for('oneitem',
                    bucketlists_id=self.bucketlist.id,
                    item_id=item.id),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

    def test_delete_item(self):
        self.client.post(
            url_for('items', bucketlists_id=self.bucketlist.id),
            data=json.dumps({
                'name': 'test_item',
                'done': False
            }),
            headers=self.token)
        item = Item.query.filter_by(name="test_item").first()
        response = self.client.delete(
            url_for('oneitem',
                    bucketlists_id=self.bucketlist.id,
                    item_id=item.id),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

        response = self.client.get(
            url_for('oneitem',
                    bucketlists_id=self.bucketlist.id,
                    item_id=item.id),
            headers=self.token)
        self.assert_status(response, 400)

    def test_search_for_item(self):
        self.client.post(
            url_for('items', bucketlists_id=self.bucketlist.id),
            data=json.dumps({
                'name': 'item1',
                'done': False,
            }),
            headers=self.token)
        response = self.client.get(
            '/api/v1/bucketlists/{}/items?q=item'.format(self.bucketlist.id),
            headers=self.token)
        self.assert_200(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)

        response = self.client.get(
            '/api/v1/bucketlists/{}/items?q=none'.format(self.bucketlist.id),
            headers=self.token)
        self.assert_status(response, 400)
        result = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(result)
        self.assertIn('No item matching the search param',
                      result['message'])

    def test_edit_item(self):
        self.client.post(
            url_for('items', bucketlists_id=self.bucketlist.id),
            data=json.dumps({
                'name': 'test_item',
                'done': False
            }),
            headers=self.token)
        item = Item.query.filter_by(name="test_item").first()
        response = self.client.put(
            url_for('oneitem',
                    bucketlists_id=self.bucketlist.id,
                    item_id=item.id),
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
            url_for('items', bucketlists_id=self.bucketlist.id),
            data=json.dumps(
                {
                    'name': 'Ziplining'
                }),
            headers=self.token)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Item already exists",
                      data['message'])

    def test_incomplete_detail_on_item(self):
        response = self.client.post(
            url_for('items', bucketlists_id=self.bucketlist.id),
            data=json.dumps({'name': ''}),
            headers=self.token)
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("provide the name",
                      data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
