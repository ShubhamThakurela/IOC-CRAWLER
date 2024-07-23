import time
from flask_restx import Resource
from flask import request, jsonify
from .dto import TelegramDto
from .telegram_services import FetchedTeleData
from .login_service import login_token_required
api = TelegramDto.api


@api.route('/search-by-keys')
class IocScrappedFetched(Resource):
    @api.doc(params={
        'channel_name': {'description': 'Specify which channel needs to Search',
                         'in': 'query', 'type': 'str'},
        'After-Date': {'description': 'Specify the start date (YYYY-MM-DD)',
                       'in': 'query', 'type': 'str'},
        'Before-Date': {'description': 'Specify the end date (YYYY-MM-DD)',
                        'in': 'query', 'type': 'str'},
        'result_keys': {'description': 'Specify which keys from the document to Get',
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
            input_type = request.args.get('channel_name')
            after_time = request.args.get('After-Date')
            before_time = request.args.get('Before-Date')
            keys_to_include = request.args.get('result_keys')
            if not input_type:
                # If the user does not select a file, the browser submits an
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the Channel Name.", }
            if not after_time:
                # If the user does not select a file, the browser submits an
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the Date.",
                }
            if not before_time:
                # If the user does not select a file, the browser submits an
                return {
                    "Status": False,
                    "Message": "Sorry! Please insert the Date.",
                }
            start_datetime = time.time()
            out_result = FetchedTeleData.fetch_by_params(input_type, after_time, before_time, keys_to_include)
            end_time = time.time()
            response = {
                "Status": True,
                'Time_Taken': '{:.3f} sec'.format(end_time - start_datetime),
                'Results': out_result}
            return response
        except Exception as e:
            print(e)
