import os
from flask_restx import Resource
from flask import request, send_file, abort, jsonify
from flask_cors import cross_origin
from .constan_service import ConstantService
from .dto import RulesDto
from .rules_service import RulesService
from .login_service import login_token_required
api = RulesDto.api


@api.route('/get-all-data')
class IocScrappedFetchedController(Resource):
    @api.doc(params={
        'rule_type': {'description': 'Rule file needs to download (yara, sigma)',
                      'in': 'query', 'type': 'str'}})
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
            rule_type_name = request.args.get('rule_type')
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
                    if os.path.exists(out_file_path):
                        return send_file(out_file_path, as_attachment=True)
                    abort(404, description="Invalid File Name, - 404 not found")
        except Exception as q:
            return q


@api.route('/fetch-by-date')
class IocScrappedFetchedController(Resource):
    @api.doc(params={
        'date': {'description': 'Date to get the file (YYYY-MM-DD)',
                 'in': 'query', 'type': 'str'},
        'rule_type': {'description': '(yara, sigma)',
                      'in': 'query', 'type': 'str'}
    })
    def post(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
            input_type = request.args.get('rule_type')
            type_of_search = request.args.get('date')
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
            out_file_path = os.path.join(ConstantService.rules_data_out_path())
            zipped_path = os.path.join(ConstantService.data_processed_path())
            zipped_file = RulesService.zip_specific_file(out_file_path, zipped_path, output_file_name)
            if not zipped_file:
                return {
                    "status": False,
                    "error": 'file not found.',
                    "message": "Error! Your downloadable Data Not prepared",
                }
            out_file_path = os.path.join(ConstantService.data_processed_path(), zipped_file)
            if os.path.exists(out_file_path):
                return send_file(out_file_path, as_attachment=True)
            abort(404, description="Invalid File Name, - 404 not found"
                  )
        except Exception as q:
            return q


@api.route('/download-file')
class IocScrappedFetchedController(Resource):
    @api.doc(params={
        'output_file_name': {'description': 'Rules file name', 'in': 'query', 'type': 'str'}})
    def get(self):
        try:
            # token_check = login_token_required()
            # if token_check["Code"] == 200:
            #     pass
            # elif token_check["Code"] == 502:
            #     return jsonify(token_check)
            # elif token_check["Code"] == 504:
            #     return jsonify(token_check)
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
                    "message": "Sorry! Please enter the file with file extension, Ex- sample.txt.",
                }
            out_file_path = os.path.join(ConstantService.data_out_path(), output_file_name)
            if os.path.exists(out_file_path):
                if out_file_path:
                    return send_file(out_file_path, as_attachment=True)
                abort(404, description="Crawled data not found")
            else:
                return "File not Found!, Please try again."
        except Exception as q:
            return q


def down(output_file_name):
    a = ".zip"
    if a in output_file_name:
        return True
    else:
        return False
