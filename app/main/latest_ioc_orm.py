from datetime import timedelta, datetime
from .db_connection import ConnectionService


class MonitorOrm:
    @staticmethod
    def run_queries_fetched_result(source_type, date_extracted):
        try:
            collection, filters_criteria = None, None
            date_string = date_extracted
            type_value = source_type
            if type_value == 'ip':
                # Connecting to Mongodb and getting Collection and client
                collection, client = ConnectionService.db_collection_ip()
                filters_criteria = {
                    'source_type': {
                        '$in': ['ip']}
                }
            elif type_value == 'domain':
                collection, client = ConnectionService.db_domains_collection()
                filters_criteria = {
                    'source_type': {
                        '$in': ['domain']}
                }

            elif type_value == 'url':
                collection, client = ConnectionService.db_url_collection()
                filters_criteria = {
                    'source_type': {
                        '$in': ['url']}
                }
            elif type_value == 'hashes':
                collection, client = ConnectionService.db_hashes_collection()
                filters_criteria = {
                    'source_type': {
                        '$in': ['hashes']}
                }
            elif type_value == 'subnet':
                collection, client = ConnectionService.db_subnet_collection()
                filters_criteria = {
                    'source_type': {
                        '$in': ['subnet']}
                }
            elif type_value == 'source':
                collection, client = ConnectionService.db_collection_source()
                filters_criteria = {
                    "source_type": type_value
                }
            query = {
                'first_timestamp': {'$regex': f'^{date_extracted}'}
            }
            result = collection.find(query)
            if result:
                documents_list = list(result)
                print("result-->", documents_list)
                return documents_list
        except Exception as e:
            print(e)
            return []
