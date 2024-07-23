from .dto import MonitorDto
import os
import time
from datetime import datetime
from flask_cors import cross_origin
from flask import send_file, abort, jsonify, make_response
from flask_restx import Resource
from werkzeug.datastructures import FileStorage
from .constan_service import ConstantService
from .login_service import login_token_required
from .monitor_services import FetchedData
from .rules_service import RulesService

api = MonitorDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/ip')
class IocIp(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            token_check = login_token_required()
            if token_check["Code"] == 200:
                pass
            elif token_check["Code"] == 404:
                return make_response(jsonify(token_check), 404)
            elif token_check["Code"] == 400:
                return make_response(jsonify(token_check), 400)
            data_fetched_date = datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_latest_path())
            start_datetime = time.time()
            source_type = 'ip'
            password = '00123'
            result_file_zipped, result_zipped_pth = FetchedData.fetch_by_params(source_type, file_path, zipped_path,
                                                                                data_fetched_date, password)
            result_zipped_pth = result_zipped_pth.replace('\\', '/')
            # zipped_path = zipped_path + "/" + str(datetime.now().date())
            # print("-->", zipped_path)
            if "no results" in result_file_zipped:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": result_file_zipped,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(result_zipped_pth, result_file_zipped)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
                else:
                    return make_response(str("File not Found!, Please try again."), 404)
        except Exception as e:
            print("error in ip -->", e)
            return make_response(str(e), 404)


@api.route('/domain')
class IocDomains(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 404:
            #     return make_response(jsonify(token_check), 404)
            # elif token_check["Code"] == 400:
            #     return make_response(jsonify(token_check), 400)
            data_fetched_date = datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_latest_path())
            start_datetime = time.time()
            source_type = 'domain'
            password = '00123'
            result_file_zipped, result_zipped_path = FetchedData.fetch_by_params(source_type, file_path, zipped_path,
                                                                                 data_fetched_date, password)
            result_zipped_path = result_zipped_path.replace('\\', '/')
            if "no results" in result_file_zipped:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": result_file_zipped,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(result_zipped_path, result_file_zipped)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
                else:
                    return make_response(str("File not Found!, Please try again."), 404)
        except Exception as e:
            print("error in domains -->", e)
            return make_response(str(e), 404)


@api.route('/hash')
class IocUrls(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 404:
            #     return make_response(jsonify(token_check), 404)
            # elif token_check["Code"] == 400:
            #     return make_response(jsonify(token_check), 400)
            data_fetched_date = datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_latest_path())
            start_datetime = time.time()
            source_type = 'hashes'
            password = '00123'
            result_file_zipped, result_zipped_pth = FetchedData.fetch_by_params(source_type, file_path, zipped_path,
                                                                                data_fetched_date, password)
            result_zipped_pth = result_zipped_pth.replace('\\', '/')
            if "no results" in result_file_zipped:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": result_file_zipped,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(result_zipped_pth, result_file_zipped)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
                else:
                    return make_response(str("File not Found!, Please try again."), 404)
        except Exception as e:
            print("error in hashes -->", e)
            return make_response(str(e), 404)


@api.route('/sigma')
class IocUrls(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            start_datetime = time.time()
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 404:
            #     return make_response(jsonify(token_check), 404)
            # elif token_check["Code"] == 400:
            #     return make_response(jsonify(token_check), 400)
            input_type = 'sigma'
            type_of_search = datetime.now().strftime("%Y-%m-%d")
            file_name = type_of_search + '-' + input_type + '_rules.txt'
            if not input_type:
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the rules file name."}
            if not type_of_search:
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the Date."}
            output_file_name = file_name
            password = '00123'
            out_file_path = os.path.join(ConstantService.rules_data_out_path())
            zipped_path = os.path.join(ConstantService.data_latest_path())
            result_file_zipped, result_zipped_pth = RulesService.rule_zipped_file(out_file_path, zipped_path,
                                                                                  output_file_name, password,
                                                                                  type_of_search,
                                                                                  input_type)
            result_zipped_pth = result_zipped_pth.replace('\\', '/')
            if "no results" in result_file_zipped:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": result_file_zipped,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(result_zipped_pth, result_file_zipped)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
                else:
                    return make_response(str("File not Found!, Please try again."), 404)

        except Exception as e:
            print("error in sigma -->", e)
            return make_response(str(e), 404)


@api.route('/url')
class IocUrls(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 404:
            #     return make_response(jsonify(token_check), 404)
            # elif token_check["Code"] == 400:
            #     return make_response(jsonify(token_check), 400)
            data_fetched_date = datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_latest_path())
            start_datetime = time.time()
            source_type = 'url'
            password = '00123'
            result_file_zipped, result_zipped_pth = FetchedData.fetch_by_params(source_type, file_path, zipped_path,
                                                                                data_fetched_date, password)
            result_zipped_pth = result_zipped_pth.replace('\\', '/')
            if "no results" in result_file_zipped:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": result_file_zipped,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(result_zipped_pth, result_file_zipped)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
                else:
                    return make_response(str("File not Found!, Please try again."), 404)
        except Exception as e:
            print("error in urls -->", e)
            return make_response(str(e), 404)


@api.route('/yara')
class IocUrls(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            start_datetime = time.time()
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 404:
            #     return make_response(jsonify(token_check), 404)
            # elif token_check["Code"] == 400:
            #     return make_response(jsonify(token_check), 400)
            input_type = 'yara'
            type_of_search = datetime.now().strftime("%Y-%m-%d")
            file_name = type_of_search + '-' + input_type + '_rules.txt'
            if not input_type:
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the rules file name."}
            if not type_of_search:
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the Date."}
            output_file_name = file_name
            password = '00123'
            out_file_path = os.path.join(ConstantService.rules_data_out_path())
            zipped_path = os.path.join(ConstantService.data_latest_path())
            result_file_zipped, result_zipped_pth = RulesService.rule_zipped_file(out_file_path, zipped_path,
                                                                                  output_file_name, password,
                                                                                  type_of_search,
                                                                                  input_type)
            result_zipped_pth = result_zipped_pth.replace('\\', '/')
            if "no results" in result_file_zipped:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": result_file_zipped,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(result_zipped_pth, result_file_zipped)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
                else:
                    return make_response(str("File not Found!, Please try again."), 404)
        except Exception as e:
            print("error in yara -->", e)
            return make_response(str(e), 404)
