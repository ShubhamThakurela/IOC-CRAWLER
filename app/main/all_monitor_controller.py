import logging
import traceback
from .dto import ALLMonitorDto
import os
import time
from flask import jsonify
from flask_cors import cross_origin
from flask import send_file, abort, make_response
from flask_restx import Resource
from werkzeug.datastructures import FileStorage
from .constan_service import ConstantService
from .login_service import login_token_required
from .ioc_service import FetchedData
from .rules_service import RulesService

api = ALLMonitorDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/ip')
class IocIp(Resource):
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
            ioc_source_type = 'ip'
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            if not ioc_source_type:
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the At-least one Source."}
            start_datetime = time.time()
            output_file = FetchedData.fetch_all_collections(ioc_source_type, file_path, zipped_path)
            if "no results" in output_file:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": output_file,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(ConstantService.data_processed_path(), output_file)
                print(out_file_path)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found"
                          )
                else:
                    return make_response(str("File not Found!, Please try again."), 404)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
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
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
            ioc_source_type = 'domain'
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            if not ioc_source_type:
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the At-least one Source."}
            start_datetime = time.time()
            output_file = FetchedData.fetch_all_collections(ioc_source_type, file_path, zipped_path)
            if "no results" in output_file:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": output_file,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(ConstantService.data_processed_path(), output_file)
                print(out_file_path)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found"
                          )
                else:
                    return "File not Found!, Please try again."
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            return make_response(str(e), 404)


@api.route('/hash')
class IocUrls(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            token_check = login_token_required()
            if token_check["Code"] == 200:
                pass
            elif token_check["Code"] == 502:
                return jsonify(token_check)
            elif token_check["Code"] == 504:
                return jsonify(token_check)
            ioc_source_type = 'hashes'
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            if not ioc_source_type:
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the At-least one Source."}
            start_datetime = time.time()
            output_file = FetchedData.fetch_all_collections(ioc_source_type, file_path, zipped_path)
            if "no results" in output_file:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": output_file,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(ConstantService.data_processed_path(), output_file)
                print(out_file_path)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found"
                          )
                else:
                    return "File not Found!, Please try again."
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))


@api.route('/sigma')
class IocUrls(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
            rule_type_name = 'sigma'
            out_file_path = os.path.join(ConstantService.rules_data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            if os.path.exists(out_file_path):
                out_put_directory = os.path.join(ConstantService.data_out_path())
                if os.path.exists(out_file_path):
                    output_directory = out_put_directory
                    result_obj = RulesService(out_file_path, rule_type_name, output_directory, zipped_path)
                    result = result_obj.write_data_into_single_file()
                    # Extract the filename from the file path
                    filename = os.path.basename(result)
                    if not result:
                        return {
                            "status": False,
                            "error": str(result),
                            "message": "Error! Your downloadable Data Not prepared",
                        }
                    out_file_path = os.path.join(ConstantService.data_processed_path(), result)
                    print(out_file_path)
                    if os.path.exists(out_file_path):
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
        except Exception as q:
            print("error in sigma -->", q)
            return "File not Found!, Please try again."


@api.route('/url')
class IocUrls(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
            ioc_source_type = 'url'
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            if not ioc_source_type:
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the At-least one Source."}
            start_datetime = time.time()
            output_file = FetchedData.fetch_all_collections(ioc_source_type, file_path, zipped_path)
            if "no results" in output_file:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": output_file,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(ConstantService.data_processed_path(), output_file)
                print(out_file_path)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found"
                          )
                else:
                    return "File not Found!, Please try again."
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))


@api.route('/yara')
class IocUrls(Resource):
    @api.doc(params={})
    @cross_origin()
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
            rule_type_name = 'yara'
            out_file_path = os.path.join(ConstantService.rules_data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            if os.path.exists(out_file_path):
                out_put_directory = os.path.join(ConstantService.data_out_path())
                if os.path.exists(out_file_path):
                    output_directory = out_put_directory
                    result_obj = RulesService(out_file_path, rule_type_name, output_directory, zipped_path)
                    result = result_obj.write_data_into_single_file()
                    # Extract the filename from the file path
                    filename = os.path.basename(result)
                    if not result:
                        return {
                            "status": False,
                            "error": str(result),
                            "message": "Error! Your downloadable Data Not prepared",
                        }
                    out_file_path = os.path.join(ConstantService.data_processed_path(), result)
                    print(out_file_path)
                    if os.path.exists(out_file_path):
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
        except Exception as q:
            print("error in yara -->", q)
            return "File not Found!, Please try again."
