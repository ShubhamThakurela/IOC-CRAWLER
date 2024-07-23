from typing import Optional
from .db_connection import ConnectionService
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError, DuplicateKeyError


class IocOrm:
    # constructor or __init__ method of the class object.
    def __init__(self, data_list):
        self.list_dicts = data_list

    def insert_or_update(self):
        """
        It takes the list of dicts as a parameter and do to insertion and update data into database
        :param self.list_dict = {}
        :return: Exception (string) it through the error and pass the execution whenever duplicate data try to insert
        """
        collection = None
        client = None
        try:
            # Example condition: Check if the first key of each dictionary is 'key1'
            for my_dict in self.list_dicts:
                first_key = next(iter(my_dict))  # Get the first key of the dictionary
                if first_key == 'ip':
                    # Connecting to Mongodb and getting Collection and client
                    collection, client = ConnectionService.db_collection_ip()
                    break
                elif first_key == 'domain':
                    collection, client = ConnectionService.db_domains_collection()
                    break
                elif first_key == 'url':
                    collection, client = ConnectionService.db_url_collection()
                    break
                elif first_key == 'hash':
                    collection, client = ConnectionService.db_hashes_collection()
                    break
                elif first_key == 'subnet':
                    collection, client = ConnectionService.db_subnet_collection()
                    break
            # Checking exist index of doc and Creating the unique index if not exist
            value_return_collection = check_and_create_index(collection, self.list_dicts)
            bulk_updates = []
            for data_dict in self.list_dicts:
                print('the data going to insert:', data_dict)
                unique_key = list(data_dict.keys())[0]
                filter_query = {unique_key: data_dict[unique_key]}
                # Step 3: Try to find a matching document
                existing_doc = collection.find(filter_query)
                if existing_doc:
                    # If matching document found, update the array keys
                    update_data = {'$set': {key: data_dict[key] for key in data_dict if key != unique_key}}
                    bulk_updates.append(UpdateOne(filter_query, update_data, upsert=True))
            if bulk_updates:
                try:
                    # Perform bulk update operation
                    collection.bulk_write(bulk_updates)
                except BulkWriteError as bwe:
                    # Handle the BulkWriteError specifically
                    for error in bwe.details['writeErrors']:
                        if error['code'] == 11000:
                            # 11000 code indicates a duplicate key error
                            # You can choose to log the error or handle it in any other way you prefer
                            print("Duplicate data! Error occurred:", error)
                    client.close()
            status = "Data Inserted Successfully!"
            return status
        except Exception as e:
            print(e)
            return str(e)

    def insert_sources(self):
        status = None
        try:
            # Connecting to Mongodb and getting Collection and client
            collection, client = ConnectionService.db_collection_source()
            # Checking exist index of doc and Creating the unique index if not exist
            # value_return_collection = check_and_create_index(collection, self.list_dicts)
            if self.list_dicts:
                try:
                    # Iterate through the list of dicts to create a list of UpdateOne operations
                    update_operations = [
                        UpdateOne({'Url': doc['Url']}, {'$set': doc}, upsert=True)
                        for doc in self.list_dicts
                    ]
                    # data_insertion = value_return_collection.insert_many(self.list_dicts, ordered=False)
                    result = collection.bulk_write(update_operations, ordered=False)
                    client.close()
                    status = "Data Inserted Successfully!"
                    return status
                except DuplicateKeyError as e:
                    # Handle the duplicate key error
                    print(f"Duplicate key error occurred: {e}")
        # Decide what you want to do when the duplicate key error occurs
        # For example, you may log the error and continue, or skip the insertion
        except Exception as e:
            print(repr(e))
            # Handle other types of exceptions if needed
            # For example, log the error and decide how to handle it
            return "An error occurred during data insertion."

    def insert_data(self):
        """
            It takes the list of dicts as a parameter and do to insertion into database
            :param: list_dicts
            :return: Exception (string) it through the error and pass the execution whenever duplicate data
             try to insert
            """
        collection = None
        client = None
        try:
            # Example condition: Check if the first key of each dictionary is 'key1'
            for my_dict in self.list_dicts:
                first_key = next(iter(my_dict))  # Get the first key of the dictionary
                if first_key == 'ip':
                    # Connecting to Mongodb and getting Collection and client
                    collection, client = ConnectionService.db_collection_ip()
                    break
                elif first_key == 'domain':
                    collection, client = ConnectionService.db_domains_collection()
                    break
                elif first_key == 'url':
                    collection, client = ConnectionService.db_url_collection()
                    break
                elif first_key == 'hash':
                    collection, client = ConnectionService.db_hashes_collection()
                    break
                elif first_key == 'subnet':
                    collection, client = ConnectionService.db_subnet_collection()
                    break
            value_return_collection = check_and_create_index(collection, self.list_dicts)
            bulk_updates = []
            for data_dict in self.list_dicts:
                print('the dicts going to insert:', data_dict)
                unique_key = list(data_dict.keys())[0]
                filter_query = {unique_key: data_dict[unique_key]}
                # Step 3: Try to find a matching document
                existing_doc = collection.find(filter_query)
                if existing_doc:
                    # If matching document found, update the array keys
                    update_data = {'$set': {key: data_dict[key] for key in data_dict if key != unique_key}}
                    bulk_updates.append(UpdateOne(filter_query, update_data, upsert=True))
            if bulk_updates:
                try:
                    # Perform bulk update operation
                    collection.bulk_write(bulk_updates)
                except BulkWriteError as bwe:
                    # Handle the BulkWriteError specifically
                    for error in bwe.details['writeErrors']:
                        if error['code'] == 11000:
                            # 11000 code indicates a duplicate key error
                            # You can choose to log the error or handle it in any other way you prefer
                            print("Duplicate data! Error occurred:", error)
                    client.close()
            status = "Data Inserted Successfully!"
            return status
        except Exception as e:
            print(e)
            return None


def login_check(collection, data):
    try:
        for key in data.keys():
            # this below codes run the condition to check whether index exists or Not
            if key not in collection.index_information():
                # Index doesn't exist, create one
                collection.create_index(key, unique=True)
                print(f"Index created for key: {key}")
                return collection
    except Exception as h:
        # Prints Exception and return representation of the object.
        print(repr(h))
        return repr(h)


class DbOrmIoc:

    @staticmethod
    def source_queries_fetched_result(source_type):
        try:
            collection, filters_criteria = None, None
            if source_type:
                collection, client = ConnectionService.db_collection_source()
                filters_criteria = {
                    "source_type": source_type
                }
            # Append the time component to the date (00:00:00.000) and create a datetime object.
            result = collection.find(filters_criteria)
            if result:
                result_list = list(result)
                return result_list
        except Exception as e:
            print(e)

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
            # Append the time component to the date (00:00:00.000) and create a datetime object.
            result = collection.find(filters_criteria)
            if result:
                return result
        except Exception as e:
            print(e)


def check_and_create_index(collection, data_dicts: Optional[dict] = None):
    """
    # It creates and checks the index of collections documents and returns the collection for inserting.
    :param collection: Name of the collection or db in which needs to be C&C.
    :param data_dicts: list of dicts for creation of indexes.
    :return: collection for db docs and Prints Exception and return representation of the object.
    """
    try:
        # Loop through all the dicts present in the list of dicts param
        for data_dict in data_dicts:
            # Loop through the keys of dicts for creating the index based on dict(key)
            for key in data_dict.keys():
                # this below codes run the condition to check whether index exists or Not
                if key not in collection.index_information():
                    # Index doesn't exist, create one
                    collection.create_index(key, unique=True)
                    print(f"Index created for key: {key}")
                    return collection
    except Exception as h:
        # Prints Exception and return representation of the object.
        print(repr(h))
        return repr(h)
