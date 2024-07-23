import jwt
from flask import session, jsonify
from datetime import datetime
from bson.objectid import ObjectId
from .db_connection import ConnectionService


class LoginClass(object):
    def __init__(self):
        pass

    @staticmethod
    def add_user(data):
        try:
            collection, client = ConnectionService.db_collection_login()
            inserted_user = collection.insert_one(data)
            usr_id = str(inserted_user.inserted_id)
            client.close()
            return "User registered successfully!", usr_id
        except Exception as e:
            print(e)

    @staticmethod
    def profile(jwt_key):
        if 'loggedin' in session:
            user_id = session['id']
            collection, client = ConnectionService.db_collection_login()
            # Retrieve the user's data from the collection
            document_id = ObjectId(user_id)
            account = collection.find_one({"_id": document_id})
            if account:
                res = {
                    "Email": account["email_id"],
                    "Name": account["name"],
                }
                # Encode the data as a JSON Web Token (JWT)
                encoded_jwt_token = jwt.encode(res, jwt_key, algorithm="HS256")
                return encoded_jwt_token
        return False


