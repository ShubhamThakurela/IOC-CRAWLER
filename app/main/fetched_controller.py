import os
import time
import traceback
import logging
from flask import request, send_file, abort, jsonify
from flask_restx import Resource
from werkzeug.datastructures import FileStorage
from .constan_service import ConstantService
from .dto import DownloadDto
from .ioc_service import FetchedData
from .login_service import login_required, login_token_required

api = DownloadDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/get-all-data')
class IocScrappedFetched(Resource):
    @api.doc(params={
        'Source': {'description': '(ip, url, hashes, domain, subnet) ',
                   'in': 'query', 'type': 'str'}})
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
            ioc_source_type = request.args.get('Source')
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
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/get-by-date')
class IocScrappedFetched(Resource):
    @api.doc(params={
        'source': {'description': '(Ex - ip, domain, url, hashes, subnet)',
                   'in': 'query', 'type': 'str'},
        'Data_extracted_Date': {'description': 'Specify the date, (YYYY-MM-DD)',
                                'in': 'query', 'type': 'str'}
    })
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
            ioc_source_type = request.args.get('source')
            data_fetched_date = request.args.get('Data_extracted_Date')
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            if not ioc_source_type:
                # If the user does not select a file, the browser submits an
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the At-least one Source .", }
            if not data_fetched_date:
                # If the user does not select a file, the browser submits an
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the Date.",
                }
            start_datetime = time.time()
            output_file_name = FetchedData.fetch_by_params(ioc_source_type, file_path, zipped_path, data_fetched_date)
            # out_file_name = ioc_source_type + ".txt"
            if "no results" in output_file_name:
                # End time
                end_time = time.time()
                return {
                    "status": False,
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "error": output_file_name,
                    "message": "Error! Your downloadable Data Not prepared",
                }
            else:
                out_file_path = os.path.join(ConstantService.data_processed_path(), output_file_name)
                if os.path.exists(out_file_path):
                    if out_file_path:
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
                else:
                    return "File not Found!, Please try again."
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


@api.route('/get-ioc-sources')
class IocScrappedFetched(Resource):
    @api.doc(params={
        'Ioc-Type': {'description': '(ip, url, hashes, domain, subnet) ',
                     'in': 'query', 'type': 'str'}})
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
            ioc_source_type = request.args.get('Ioc-Type')
            file_path = os.path.join(ConstantService.data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            if not ioc_source_type:
                # If the user does not select a file, the browser submits an
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the At-least one Source."}
            start_datetime = time.time()
            output_file = FetchedData.fetch_only_sources(ioc_source_type)
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
                # End time
                end_time = time.time()
                return {
                    "status": True,
                    "message": "Success! Your Data Fetched!",
                    'time_taken': '{:.3f} sec'.format(end_time - start_datetime),
                    "result": output_file,
                }
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


@api.route('/download-file')
class SourceDownloadController(Resource):
    @api.doc(params={
        'output_file_name': {'description': 'Scrape_Downloader crawled data output zip file name', 'in': 'query',
                             'type': 'str'}})
    def get(self):
        token_check = login_token_required()
        if token_check["Code"] == 200:
            pass
        elif token_check["Code"] == 502:
            return jsonify(token_check)
        elif token_check["Code"] == 504:
            return jsonify(token_check)
        if request.args.get('output_file_name', None) is None:
            return {
                "status": False,
                "message": "Sorry! Please Enter Valid File Name."
            }
        output_file_name = request.args.get('output_file_name')
        down(output_file_name)
        res = down(output_file_name)
        if res is True:
            pass
        else:
            return {
                "status": False,
                "message": "Sorry! Please enter Scrape_Downloader data output file name.",
            }
        out_file_path = os.path.join(ConstantService.data_processed_path(), output_file_name)
        if os.path.exists(out_file_path):
            return send_file(out_file_path, as_attachment=True)
        abort(404, description="Invalid File Name, - 404 not found")


def down(output_file_name):
    a = ".zip"
    if a in output_file_name:
        return True
    else:
        return False
