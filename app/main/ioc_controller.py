import logging
import os
import shutil
import time
import pandas as pd
from flask import jsonify
from flask import request
from flask_restx import Resource
from werkzeug.datastructures import FileStorage
from .constan_service import ConstantService
from .dto import IocDto
from .ioc_service import IocService
from .login_service import login_required, login_token_required

api = IocDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/crawl-url')
class IocUrl(Resource):
    @api.doc(params={
        'url': {'description': 'website url', 'in': 'query', 'type': 'str'},
        'extraction_type': {'description': 'Specify whether ioc need to scrap individually  or not, If True then '
                                           'mention ioc_name_type param', 'in': 'query',
                            'type': 'boolean', 'default': 'false'},
        'ioc_name': {'description': 'If Ext _type - False, Specify ioc names to scrap (ip, domain, url, hashes, '
                                    'subnet, all)',
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
            # login_result = login_required()
            start_time = time.time()
            url = request.args.get('url')
            data_extraction_type = request.args.get('extraction_type')
            if data_extraction_type == 'false':
                ioc_type_argue = ['all']
                source_data = IocService.crawl_all_ioc(url, ioc_type_argue)
                end_time_2 = time.time()
                if not source_data:
                    response = {
                        "status": False,
                        'time_taken': '{:.3f} sec'.format(end_time_2 - start_time),
                        "message": "Error! Your source url crawled Task Failed, Please try again!",
                        "request_result": source_data,
                        "Processed Url": url
                    }
                    return jsonify(response)
                else:
                    # End time
                    end_time = time.time()
                    response = {
                        "status": True,
                        'time_taken': '{:.3f} sec'.format(end_time - start_time),
                        "message": "Congratulations! Your source url crawled successfully.",
                        "request_result": source_data,
                        "Processed Url": url
                    }
                    return jsonify(response)
            else:
                ioc_type_argue = request.args.__getitem__('ioc_name')
                extraction_result = IocService.crawl_single_ioc_url(url, ioc_type_argue)
                end_time_2 = time.time()
                if not extraction_result:
                    response = {
                        "status": False,
                        'time_taken': '{:.3f} sec'.format(end_time_2 - start_time),
                        "message": "Error! Your source url crawled Task Failed, Please try again!",
                        "request_result": extraction_result,
                        "Processed Url": url
                    }
                    return jsonify(response)
                else:
                    # End time
                    end_time = time.time()
                    response = {
                        "status": True,
                        'time_taken': '{:.3f} sec'.format(end_time - start_time),
                        "message": "Congratulations! Your source url crawled successfully.",
                        "request_result": extraction_result,
                        "Processed Url": url
                    }
                    return jsonify(response)
        except Exception as e:
            print(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            # If any Exception Occurred it will return the Exception in json
            return jsonify(response)


def url_source(source):
    web = ['ip', 'domain', 'hashes', 'url', 'subnet', 'all']
    if source in web:
        return str("OK")
    else:
        return False


def rl(url):
    a = "http"
    if a in url:
        return str("ok_url")
    else:
        return str("Invalid_url")


@api.route('/crawl-file')
@api.expect(upload_parser)
class IocFile(Resource):
    """
    This Class Handle the Api Controller and all the Curd operations Using api Rest Methods
    """

    # Doc Param: "Tips Information Block"
    @api.doc(params={})
    def post(self):
        # token_check = login_token_required()
        # if token_check["Code"] == 200:
        #     pass
        # elif token_check["Code"] == 502:
        #     return jsonify(token_check)
        # elif token_check["Code"] == 504:
        #     return jsonify(token_check)a
        # Checks the file uploaded or not before processing
        if 'file' not in request.files:
            # If the user does not select a file, the browser submits an
            return {
                "Status": False,
                "Message": "Sorry! file not passed.",
            }
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        if file.filename == '':
            return {
                "Status": False,
                "Message": "Sorry! file not passed.",
            }
        # Fetching the file path from the Constant Class objects to process furthers
        file_path = ConstantService.data_in_path() + '/' + file.filename
        # saving the file in drive in folder path
        file.save(file_path)
        # applying file Validation to check whether it is in a correct format and extension
        res = file_ext_validation(file_path)
        if res is True:
            pass
        else:
            return res
        # applying file Validation to check whether it is in a correct format before processing.
        res = validation(file_path)
        if res is True:
            pass
        else:
            # if res is not true it will remove the file from (In) folder path
            os.remove(file_path)
            # If the user does not maintain the correct file format, the browser submits an
            return {
                "status": False,
                "message": "Url Type Name Should be - ip, domain, hashes and url, Sorry file not passed.",
            }
        try:
            # Main workflow Execution starts here..//////
            start_time = time.time()
            # Calling the Service Class (IocService) objects to extracts the data and to complete workflow
            status = IocService.crawl_by_file(file_path)
            # Move file to processed after completed the process
            if not os.path.exists(os.path.dirname(ConstantService.data_processed_path())):
                os.makedirs(os.path.dirname(ConstantService.data_processed_path()))
            shutil.move(file_path, os.path.join(ConstantService.data_processed_path(), os.path.basename(file_path)))
            # Program workflow Ends Here!
            end_time = time.time()
            status_validation = status[1]
            if "403" in status_validation:
                # Sending the Json Response to the Request, Responding with Json
                response = {
                    "Status": False,
                    "Result": status,
                    "Message": "Failed! Your file crawled Failed.",
                    "File Processed Time": '{:.3f} sec'.format(end_time - start_time),
                    "File": file.filename
                }
                return jsonify(response)
            elif not status:
                # Sending the Json Response to the Request, Responding with Json
                response = {
                    "Status": False,
                    "Result": status,
                    "Message": "Failed! Your file crawled Failed.",
                    "File Processed Time": '{:.3f} sec'.format(end_time - start_time),
                    "File": file.filename
                }
                return jsonify(response)
            else:
                # Sending the Json Response to the Request, Responding with Json
                response = {
                    "Status": True,
                    "Result": status,
                    "Message": "Congratulations! Your file crawled successfully.",
                    "File Processed Time": '{:.3f} sec'.format(end_time - start_time),
                    "File": file.filename
                }
                return jsonify(response)
        except Exception as e:
            print(str(e))
            logging.error(str(e))


def file_ext_validation(file_path):
    """
    :param file_path: Path of the parsing file
    :return: Its returns the validations Strings applied on the file
    """
    name, file_type = os.path.splitext(file_path)
    file_type = file_type.lower()
    if file_type in ['.xls', '.xlsx']:
        return True
    else:
        return "Unsupported file extension " + file_type + "! System Supporting only (.xls, .xlsx)."


def validation(file_path):
    """
    :param file_path: Path of the parsing file
    :return: Its returns the validations Strings applied on the file Returns True if all passed
    """
    name, file_type = os.path.splitext(file_path)
    file_type = file_type.lower()
    if file_type in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    elif file_type == '.csv':
        df = pd.read_csv(file_path)
    else:
        print("Unsupported file extension " + file_type + "! We are supporting only (csv, xls, xlsx).")
        return False
    url_type_com = ["ip", "hashes", "url", "domain"]
    for i in df.loc[:, "type"]:
        if i in url_type_com:
            continue
    return True
