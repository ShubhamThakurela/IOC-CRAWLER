from .telegram_orm import DbOrmTelegram
import json
from bson import ObjectId


# Function to convert ObjectId to a serializable format
def convert_id_str(doc):
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc


class FetchedTeleData:
    @staticmethod
    def fetch_by_params(input_type, after_time, before_time, keys_to_include):
        json_serializable_records = None
        try:
            fetched_results = DbOrmTelegram.run_queries_fetched_result(input_type, after_time, before_time)
            if fetched_results:
                record_list = list(fetched_results)
                # Convert all ObjectId fields in each document
                json_serializable_records = [convert_id_str(document) for document in record_list]
                # Serialize the list of documents to JSON
                json_data = json.dumps(json_serializable_records)
                dicts_list = []
                # Check the records in the list
                for document in record_list:
                    if document:
                        # Get the items from the dictionary and convert them to a list
                        items_list = list(document.items())
                        # Check if the list has at least one item
                        if len(items_list) > 1:
                            # Get the item at index 1 (the second item in the list)
                            if keys_to_include == 'post':
                                return json_data
                            elif keys_to_include == 'channel':
                                channel = items_list[1]
                                time = items_list[13]
                                result_dict = {
                                    "channel": channel[1],
                                    'time': time[1]
                                }
                                dicts_list.append(result_dict)
                            elif keys_to_include == 'timerange':
                                channel = items_list[1]
                                post_item = items_list[2]
                                time = items_list[13]
                                m_txt = items_list[12]
                                result_dict = {
                                    "channel": channel[1],
                                    'post-id': post_item[1],
                                    'time': time[1],
                                    'message-text': m_txt[1]
                                }
                                print(result_dict)
                                dicts_list.append(result_dict)
                return dicts_list
        except Exception as q:
            print(q)
