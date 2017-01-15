import json
import jwt
from app import db
from app.bucketlist.models import Bucketlist, Item
from config import Config
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource, abort


def decode_token(request):
    """
        Global function that ensures that  will be used to decode the token
    """

    token = request.headers.get('Authorization')
    if token is None:
        abort(401, message="No token provided")
    try:
        payload = jwt.decode(token, Config.SECRET_KEY)
    except jwt.DecodeError:
        abort(401, message="Token is invalid")
    except jwt.ExpiredSignature:
        abort(401, message="Token has expired")

    return payload['sub']


def display_formating(bucketlists):
    bucketlist_list = []
    for bucketlist in bucketlists.items:
        item_list = []
        items = Item.query.filter_by(
            bucketlist_id=bucketlist.id).all()
        for item in items:
            item_list.append({
                "id": item.id,
                "name": item.name,
                "date_created": item.date_created,
                "date_modified": item.date_modified,
                "done": item.done
            })
        result = {
            "id": bucketlist.id,
            "name": bucketlist.name,
            "items": item_list,
            "date_created": bucketlist.date_created,
            "date_modified": bucketlist.date_modified,
            "creator": bucketlist.creator.username
        }
        bucketlist_list.append(result)
    return bucketlist_list


def display_item_formation(bucketlist_items):
    item_list = []
    for item in bucketlist_items.items:
        item_list.append({
            "id": item.id,
            "name": item.name,
            "date_created": item.date_created,
            "date_modified": item.date_modified,
            "done": item.done
        })

    return item_list


class Bucketlists(Resource):
    """
    This class contains the get and post function.
    """

    def get(self):
        bucketlist_list = []
        user_id = decode_token(request)
        query_dict = request.args.to_dict()
        limit = int(query_dict.get('limit', 20))
        page_number = int(query_dict.get('page', 1))

        if type(limit) is not int:
            abort(400, messages="Limit must be an integer")
        if type(page_number) is not int:
            abort(400, messages="Limit must be an integer")

        if 'q' in query_dict:
            search_res = Bucketlist.query.filter(
                Bucketlist.name.ilike("%{}%".format(
                    query_dict['q']))).filter_by(
                created_by=user_id).paginate(page_number, limit)

            if not len(search_res.items):
                abort(400, message="No bucketlist matching the search param")
            bucketlist_list = display_formating(search_res)

            return jsonify(bucketlist_list)

        bucketlist = Bucketlist.query.filter_by(created_by=user_id).paginate(
            page_number, limit)
        if bucketlist is None:
            abort(
                400,
                message="No bucketlists.")
        bucketlist_list = display_formating(bucketlist)
        next_page = 'None'
        previous_page = 'None'
        if bucketlist.has_next:
            next_page = '{}api/v1/bucketlists?limit={}&page={}'.format(
                str(request.url_root),
                str(limit),
                str(page_number + 1))
        if bucketlist.has_prev:
            previous_page = '{}api/v1/bucketlists?limit={}&page={}'.format(
                str(request.url_root),
                str(limit),
                str(page_number - 1))
        return jsonify({'bucketlists': bucketlist_list,
                        'total pages': bucketlist.pages,
                        'previous': previous_page,
                        'next': next_page})

    def post(self):
        user_id = decode_token(request)
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed")
        name = data['name']
        if not name:
            abort(
                400,
                message="Kindly provide the name")
        bucketlist = Bucketlist.query.filter_by(
            name=name,
            created_by=user_id).all()

        if bucketlist:
            abort(400, message="Bucketlist already exists")
        try:
            new_bucketlist = Bucketlist(
                name=name,
                created_by=user_id
            )
            db.session.add(new_bucketlist)
            db.session.commit()
            return jsonify({
                'message': "{} created bucketlist successfully".format(name)})

        except Exception:
            abort(500, message="Bucketlist not created")


class OneBucketlist(Resource):
    """
    This class contains the get, put and delete function.
    """

    def get(self, bucketlists_id):
        user_id = decode_token(request)
        item_list = []
        bucketlist = Bucketlist.query.filter_by(
            created_by=user_id,
            id=bucketlists_id).first()
        if not bucketlist:
            abort(
                400,
                message="No bucketlist with the id {}".format(bucketlists_id))
        items = Item.query.filter_by(
            bucketlist_id=bucketlists_id).all()
        for item in items:
            item_list.append({"name": item.name,
                              "date_created": item.date_created,
                              "date_modified": item.date_modified,
                              "done": item.done})

        return jsonify({"name": bucketlist.name,
                        "created by": bucketlist.creator.username,
                        "date ceated": bucketlist.date_created,
                        "date_modified": bucketlist.date_modified,
                        "items": item_list})

    def put(self, bucketlists_id):
        user_id = decode_token(request)
        if bucketlists_id is None:
            abort(400, message="Missing bucketlist ID")
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed.Kindly fill \
                the name and description.")

        single_bucketlist = Bucketlist.query.filter_by(
            created_by=user_id, id=bucketlists_id).first()
        if not single_bucketlist:
            abort(400, message="No bucketlist matching the id {}".format(
                bucketlists_id))

        try:
            if 'name' in data.keys():
                single_bucketlist.name = data['name']
            single_bucketlist.date_modified = datetime.utcnow()
            db.session.add(single_bucketlist)
            db.session.commit()
            return jsonify({
                'message': "{} bucketlist updated successfully".format(
                    single_bucketlist.name)})
        except Exception:
            abort(500, message="Bucketlist not updated")

    def delete(self, bucketlists_id):
        user_id = decode_token(request)
        bucketlist = Bucketlist.query.filter_by(
            created_by=user_id, id=bucketlists_id).one()
        if bucketlist is None:
            abort(400, message="Bucketlist does not exist")
        try:
            db.session.delete(bucketlist)
            db.session.commit()
            return jsonify({
                "message": "{} bucketlist successfully deleted".format(
                    bucketlist.name)})
        except Exception:
            abort(500, message="Bucketlist not deleted")


class BucketlistItem(Resource):
    """
    This class contains the get and post function for items.
    """

    def get(self, bucketlists_id):
        item_list = []
        user_id = decode_token(request)
        query_dict = request.args.to_dict()
        limit = int(query_dict.get('limit', 20))
        page_number = int(query_dict.get('page', 1))

        if type(limit) is not int:
            abort(400, messages="Limit must be an integer")
        if type(page_number) is not int:
            abort(400, messages="Limit must be an integer")

        bucketlist = Bucketlist.query.filter_by(
            created_by=user_id,
            id=bucketlists_id).first()

        if bucketlist is None:
            abort(400, message="Invalid bucketlist id provided")

        if 'q' in query_dict:
            search_res = Item.query.filter(
                Item.name.ilike("%{}%".format(
                    query_dict['q']))).filter_by(
                bucketlist_id=bucketlists_id).paginate(page_number, limit)
            if not len(search_res.items):
                abort(400, message="No item matching the search param")
            item_list = display_item_formation(search_res)

            return jsonify(item_list)

        items_result = Item.query.filter_by(
            bucketlist_id=bucketlists_id).paginate(
            page_number, limit)
        if not len(items_result.items):
            abort(
                400,
                message="No items.")
        item_list = display_item_formation(items_result)
        next_page = 'None'
        previous_page = 'None'

        if items_result.has_next:
            next_page = '{}api/v1/bucketlists/{}/items?limit={}&page={}'.format(
                str(request.url_root),
                str(bucketlists_id),
                str(limit),
                str(page_number + 1))
        if items_result.has_prev:
            previous_page = '{}api/v1/bucketlists/{}/items?limit={}&page={}'.format(
                str(request.url_root),
                str(bucketlists_id),
                str(limit),
                str(page_number - 1))
        return jsonify({
            "bucketlist_name": bucketlist.name,
            'items': item_list,
            'total pages': items_result.pages,
            'previous': previous_page,
            'next': next_page})

    def post(self, bucketlists_id):
        user_id = decode_token(request)
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed")
        name = data['name']
        if not len(name):
            abort(
                400,
                message="Kindly provide the name")
        bucketlist = Bucketlist.query.filter_by(
            created_by=user_id,
            id=bucketlists_id).first()

        if bucketlist is None:
            abort(400, message="Invalid bucketlist id provided")

        item = Item.query.filter_by(name=name).first()
        if item:
            abort(400, message="Item already exists")
        try:
            new_bucketlist_item = Item(
                name=name,
                bucketlist_id=bucketlist.id
            )
            db.session.add(new_bucketlist_item)
            db.session.commit()
            return jsonify({
                'message': "{} created bucketlist item successfully".format(name)})

        except Exception:
            abort(500, message="Bucketlist not created")


class OneBucketListItem(Resource):
    """
    This class contains the get, post, put and delete function.
    """

    def get(self, bucketlists_id, item_id):
        user_id = decode_token(request)
        done = False
        if bucketlists_id is None:
            abort(400, message="Missing bucketlist ID")
        if item_id is None:
            abort(400, message="Missing item ID")

        bucketlist = Bucketlist.query.filter_by(
            created_by=user_id,
            id=bucketlists_id).first()
        if not bucketlist:
            abort(
                400,
                message="No bucketlist with the id {}".format(bucketlists_id))
        single_item = Item.query.filter_by(
            bucketlist_id=bucketlists_id,
            id=item_id).first()

        if not single_item:
            abort(400,
                  message="No item matching the id {} in the bucketlist".format(
                      item_id))
        if int(single_item.done):
            done = True

        return jsonify({"name": single_item.name,
                        "date ceated": single_item.date_created,
                        "date_modified": single_item.date_modified,
                        "done": done})

    def put(self, bucketlists_id, item_id):
        decode_token(request)
        if bucketlists_id is None:
            abort(400, message="Missing bucketlist ID")
        if item_id is None:
            abort(400, message="Missing item ID")
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed.Kindly fill the name and description.")

        single_item = Item.query.filter_by(
            bucketlist_id=bucketlists_id,
            id=item_id).first()

        if not single_item:
            abort(400, message="No bucketlist matching the id {}".format(
                bucketlists_id))

        try:
            if 'name' in data.keys():
                single_item.name = data['name']
            if 'done' in data.keys():
                single_item.done = data['done']
            single_item.date_modified = datetime.utcnow()
            db.session.add(single_item)
            db.session.commit()
            return jsonify({
                'message': "{} item updated successfully".format(
                    single_item.name)})
        except Exception:
            abort(500, message="Item not updated")

    def delete(self, bucketlists_id, item_id):
        decode_token(request)
        if bucketlists_id is None:
            abort(400, message="Missing bucketlist ID")
        if item_id is None:
            abort(400, message="Missing item ID")
        single_item = Item.query.filter_by(
            bucketlist_id=bucketlists_id,
            id=item_id).first()
        if not single_item:
            abort(400, message="No item matching the id {}".format(
                item_id))
        try:
            db.session.delete(single_item)
            db.session.commit()
            return jsonify({
                'message': "{} item deleted successfully".format(
                    single_item.name)})
        except Exception:
            abort(500, message="Item not deleted")
