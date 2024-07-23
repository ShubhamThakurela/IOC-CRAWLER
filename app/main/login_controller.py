import json
import logging
import traceback
from datetime import datetime

from flask import request, jsonify, session
from flask_restx import Resource
from werkzeug.datastructures import FileStorage
from flask_cors import cross_origin
from .login_config import LoginConfig
from .login_orm import LoginClass
from .login_service import login_required, loginService, login_token_required
from .dto import LoginDto

api = LoginDto.api

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)
upload_parser.add_argument('source', location='query', type=str)

login_obj = LoginConfig()


@api.route('/add-user')
class Login(Resource):
    @api.doc(params=({'Email': {'description': "User mail_id", 'in': 'query', 'type': 'str'},
                      'Password': {'description': "Password", 'in': 'query', 'type': 'str'},
                      'Name': {'description': "Name", 'in': 'query', 'type': 'str'},
                      'Designation': {'description': "Name", 'in': 'query', 'type': 'str'}}))
    def post(self):
        try:
            data = {
                "email_id": request.args.get('Email'),
                'password': request.args.get('Password'),
                "name": request.args.get('Name'),
                "designation": request.args.get('Designation')
            }
            email = data.get("email_id")
            name = data.get("name")
            token_check = login_token_required()
            if token_check["Code"] == 200:
                pass
            elif token_check["Code"] == 502:
                return jsonify(token_check)
            elif token_check["Code"] == 504:
                return jsonify(token_check)
            adding_user, id = LoginClass.add_user(data)
            if adding_user == "User registered successfully!":
                return {
                    "Status": 200,
                    "Message": "User successfully added",
                    "Login_id": email,
                    "Name": name,
                    'id': id
                }
            else:
                return {
                    "Status": 201,
                    "Message": "Error while adding new User",
                    "Result": adding_user
                }
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))


@api.route('/login')
class Login(Resource):
    @api.doc(params=({'Email': {'description': "User mail_id", 'in': 'query', 'type': 'str'},
                      'Password': {'description': "Password", 'in': 'query', 'type': 'str'},
                      }))
    @cross_origin()
    def get(self):
        try:
            email_id = request.args.get('Email')
            password = request.args.get('Password')
            real_login_time = datetime.now().isoformat()
            status, login_status = loginService.login_check(email_id, password)
            if status:
                jwt_key = login_obj.get_jwt_key()
                token = loginService.Profile_check(jwt_key)
                login_status_user = login_status
                response = {
                    "Status": "Accessed",
                    "Code": 200,
                    "Message": str(login_status),
                    "User_name": str(status),
                    "token": str(token)
                }
                return jsonify(response)
            else:
                response = {
                    "Status": status,
                    "Message": "Incorrect username/password!",
                    "Result": {},
                    "Info": "Please Provide Correct Creds"
                }
                return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/logout')
class ShowRecord(Resource):
    @cross_origin()
    def get(self):
        try:
            session.clear()
            response = {
                "Message": "logout successfully",
            }
            return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/update-user')
class UpdateUser(Resource):
    @api.doc(params={'email_id': 'User_id', 'Password': 'password'})
    def put(self):
        try:
            token_check = login_token_required()
            if token_check["Code"] == 200:
                pass
            elif token_check["Code"] == 502:
                return jsonify(token_check)
            elif token_check["Code"] == 504:
                return jsonify(token_check)
            data = {
                "email_id": request.args.get('email_id'),
                "password": request.args.get('Password'),
            }
            user_mail = data.get("email_id")
            result = loginService.update_record(data, user_mail)
            if result:
                response = {
                    "Status": 200,
                    "Updated_data": result,
                }
                return jsonify(response)
            else:
                response = {
                    "Status": 102,
                    "Message": "User Not Updated",
                    "Error": result,
                    "User": user_mail
                }
                return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/remove-user')
class RemoveUser(Resource):
    @api.doc(params={'email_id': 'User_id'})
    def delete(self):
        try:
            token_check = login_token_required()
            if token_check["Code"] == 200:
                pass
            elif token_check["Code"] == 502:
                return jsonify(token_check)
            elif token_check["Code"] == 504:
                return jsonify(token_check)
            emp_id = request.args.get("email_id")
            if emp_id:
                data = emp_id
                result = loginService.delete_user(data)
                if result is True:
                    responses = {
                        "Status": True,
                        "Message": "User Deleted Successfully",
                        "Code": 200,
                        "user": emp_id
                    }
                    return jsonify(responses)
                else:
                    responses = {
                        "Status": False,
                        "Message": "Please Enter a Correct User email_id",
                        "Code": 404,
                        "Error": result
                    }
                    return jsonify(responses)
            else:
                responses = {
                    "Status": False,
                    "Message": "Please Enter a User email_id",
                    "Code": 404,
                }
                return jsonify(responses)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)
