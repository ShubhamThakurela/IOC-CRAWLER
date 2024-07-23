import logging
import traceback


from .login_config import LoginConfig
from flask import session, jsonify, request

from .db_connection import ConnectionService
from .login_orm import LoginClass

login_obj = LoginConfig()


class loginService(object):
    def __init__(self):
        pass

    @staticmethod
    def Profile_check(jwt_key):
        token = LoginClass.profile(jwt_key)
        return token

    @staticmethod
    def login_check(email_id, password):
        collection, client = ConnectionService.db_collection_login()
        user = collection.find_one({"email_id": email_id,
                                    "password": password})
        if user:
            user_id = str(user["_id"])
            # Set session items with expiration time
            # session.permanent = True
            # app.permanent_session_lifetime = timedelta(hours=2)
            session['loggedin'] = True
            session['id'] = user_id
            session['username'] = user['name']
            session['role'] = user['designation']
            return session['username'], "logged_in Successfully!"
        else:
            return False, "Please check the creds"

    @staticmethod
    def update_record(data, email_id):
        try:
            collection, client = ConnectionService.db_collection_login()
            if not email_id:
                return "Missing 'email_id' in the data."
            updated_user = collection.update_one({"email_id": email_id}, {"$set": data})
            if updated_user.modified_count > 0:
                return "User data updated successfully!"
            else:
                return "User data update failed. User not found."
        except Exception as e:
            print(e)

    @staticmethod
    def delete_user(data):
        try:
            collections, client = ConnectionService.db_collection_login()
            delete_result = collections.delete_one({"email_id": data})
            if delete_result.deleted_count > 0:
                return "User deleted successfully!"
            else:
                return "User not found or already deleted."
        except Exception as k:
            print(k)


def login_token_required():
    try:
        # request_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJFbWFpbCI6InN1YmgudEBnbWwuY29tIiwiTmFtZSI6InN0In0
        # .gxBS5ncQDfdb7Ho0Cg99zT40-nOe53EGT5kXW2e3uBM"
        request_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not request_token:
            response = {
                "Status": False,
                "Code": 404,
                "error": "JW Token Missing."
            }
            return response
        else:
            jwt_key = login_obj.get_jwt_key()
            current_session_token = loginService.Profile_check(jwt_key)
            # Decode the JWT for verification or further processing
            # decoded_payload = jwt.decode(request_token, jwt_key, algorithms=["HS256"])
            if current_session_token != request_token:
                response = {
                    "Status": False,
                    "Code": 400,
                    "error": "Invalid JW Token."
                }
                return response
            else:
                response = {
                    "Status": True,
                    "Code": 200,
                    "Message": "JW Token Verified!."
                }
                return response
    except Exception as e:
        print(str(traceback.format_exc()))
        logging.error(str(e))
        return str(e)


def login_required():
    try:
        if 'loggedin' in session:
            if session['loggedin']:
                print(session)
                return True
            else:
                return False
    except Exception as e:
        print(str(traceback.format_exc()))
        logging.error(str(e))
