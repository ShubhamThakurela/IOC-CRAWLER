import json
import os
import time
# import app.main.proxy as proxy
from .latest_ioc_orm import MonitorOrm
from bson import Binary
import binascii
import hashlib
import py7zr
# import zipfile
import pyzipper
from datetime import datetime


class FetchedData:
    @staticmethod
    def fetch_by_params(source_type, file_path, zipped_path, date_extracted, password):
        try:
            ioc_type = source_type
            fetched_results = MonitorOrm.run_queries_fetched_result(ioc_type, date_extracted)
            if fetched_results:
                date_time_obj = time.strftime("%Y-%m-%d")
                # Create the filename by concatenating date_time_obj and ioc_type
                filename = f"{date_time_obj}-{ioc_type}.txt"
                file_path = file_path.replace('\\', '/')
                # Write the custom line at the beginning of the file
                with open(file_path + '/' + filename, 'w') as file:
                    # Loop through the documents and write them to the file
                    for document in fetched_results:
                        if document:
                            print(document)
                            if source_type == 'hashes':
                                if 'hash' in document and isinstance(document['hash'], Binary):
                                    json_data = FetchedData.process_document(document)
                                    binary_rm_data = json.loads(json_data)
                                    if binary_rm_data['hash'] in document:
                                        # Extract the key-value pair
                                        key_value_pair = {binary_rm_data['hash']: binary_rm_data['hash']}
                                        # Write the key-value pair as a JSON object to the file
                                        file.write(json.dumps(key_value_pair) + '\n')
                                else:
                                    if document:
                                        dict_items = list(document.items())
                                    # Check if index 2 is within the bounds of the list
                                    if 1 < len(dict_items):
                                        # Access index 2 tuple
                                        value_at_index_2 = dict_items
                                        value_at_index_2 = value_at_index_2[1][1]
                                        # print(value_at_index_2)
                                        # Write the first key-value pair as a JSON object to the file
                                        file.write(json.dumps(value_at_index_2) + '\n')
                            else:
                                if document:
                                    dict_items = list(document.items())
                                # Check if index 2 is within the bounds of the list
                                if 1 < len(dict_items):
                                    # Access index 2 tuple
                                    value_at_index_2 = dict_items
                                    value_at_index_2 = value_at_index_2[1][1]
                                    # print(value_at_index_2)
                                    # Write the first key-value pair as a JSON object to the file
                                    file.write(json.dumps(value_at_index_2) + '\n')
                # Create the date folder before calling the function
                date_folder_path = os.path.join(zipped_path, date_extracted)
                if not os.path.exists(date_folder_path):
                    os.makedirs(date_folder_path)
                archived, archived_path = FetchedData.create_password_protected_archive(file_path, date_folder_path,
                                                                                        filename, ioc_type, password)
                return archived, archived_path
            else:
                db_result = "No Document found!, Try again"
                return "no results", "no results"
        except Exception as e:
            print("error in fetch by params --> ", e)
            return "no results"

    @staticmethod
    def create_password_protected_archive(input_folder, date_folder_path, file_name, source_type, password):
        try:
            # checking the existing archived.
            existing_archive = FetchedData.get_existing_archive(date_folder_path, source_type)
            if existing_archive:
                return existing_archive, date_folder_path
            # Validate that the file exists in the input folder
            input_file_path = os.path.join(input_folder, file_name)
            if not os.path.exists(input_file_path):
                raise FileNotFoundError(
                    f"The specified file '{file_name}' does not exist in the folder '{input_folder}'.")
            # Create a password-protected .7z archive from the text file
            # password_protected_archive_name = f"_{source_type}.tar.bz2"
            password_protected_archive_name = f"_{source_type}.zip"
            password_protected_archive_path = os.path.join(date_folder_path, password_protected_archive_name)
            with pyzipper.AESZipFile(password_protected_archive_path, 'w', compression=pyzipper.ZIP_DEFLATED,
                                     encryption=pyzipper.WZ_AES) as zip_file:
                zip_file.pwd = str(password).encode()
                zip_file.write(input_file_path, arcname=file_name)

            # Calculate sha256 hash value of the password-protected archive
            sha256_hash = hashlib.sha256()
            with open(password_protected_archive_path, "rb") as file:
                for byte_block in iter(lambda: file.read(4096), b""):
                    sha256_hash.update(byte_block)
            hash_value = sha256_hash.hexdigest()

            # Rename the password-protected archive using the hash value
            # final_archive_name = f"{hash_value}_{source_type}.tar.bz2"
            final_archive_name = f"{hash_value}_{source_type}.zip"
            final_archive_path = os.path.join(date_folder_path, final_archive_name)
            os.rename(password_protected_archive_path, final_archive_path)
            # Return the name of the created password-protected archive
            final_archive_path = final_archive_path.replace(f"{final_archive_name}", '')
            return final_archive_name, final_archive_path
        except Exception as e:
            print(e)

    @staticmethod
    def process_document(doc):
        # Check if the document contains a 'hash' field, and it is of type Binary
        if 'hash' in doc and isinstance(doc['hash'], Binary):
            # Convert the Binary data to a hexadecimal string
            doc['hash'] = binascii.hexlify(doc['hash']).decode('utf-8')
        # Serialize the modified document to JSON
        json_data_1 = json.dumps(doc, default=str)
        return json_data_1

    @staticmethod
    def get_existing_archive(date_folder_path, source_type):
        try:
            # Get a list of all files in the date folder
            files_in_date_folder = os.listdir(date_folder_path)

            # Filter files based on the specified pattern
            matching_files = [file_name for file_name in files_in_date_folder if f"_{source_type}.zip" in file_name]

            # Return the first matching file if found
            if matching_files:
                return matching_files[0]
            else:
                return None
        except Exception as e:
            print(e)
