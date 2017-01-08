from flask_restful import Resource


class Bucketlist(Resource):

    def get(self):
        return {"message": "Here are all your bucketlists!!"}

    def post(self):
        return {"message": "Create new bucketlist!"}


class OneBucketlist(Resource):

    def get(self):
        return {"message": "Here are all your bucketlists!!"}

    def post(self):
        return {"message": "Create new bucketlist!"}

    def put(self):
        return {"message": "Update bucketlist!"}

    def delete(self):
        return {"message": "Delete bucketlist!"}


class Items(Resource):

    def get(self):
        return {"message": "Here are all items for the bucketlist!!"}

    def post(self):
        return {"message": "Create new items in bucketlist!"}


class OneBucketListItem(Resource):

    def get(self):
        return {"message": "Here are all items for the bucketlist!!"}

    def post(self):
        return {"message": "Create new items in bucketlist!"}

    def put(self):
        return {"message": "Update new items in bucketlist!"}

    def delete(self):
        return {"message": "Delete new item from bucketlist?"}
