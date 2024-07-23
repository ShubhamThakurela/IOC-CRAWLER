import os
import re
import tarfile
import zipfile
from .monitor_services import FetchedData


class RulesService(object):
    def __init__(self, results_file_path, rule_type_name, output_directory, zipped_path):
        self.all_files_path = results_file_path
        self.rule_type_name = rule_type_name
        self.output_directory = output_directory
        self.zipped_path = zipped_path

    def get_all_files_name(self):
        try:
            # List all files in the folder
            file_names = os.listdir(self.all_files_path)
            # Print the file names
            for file_name in file_names:
                print(file_name)
            return file_names
        except Exception as w:
            print(w)

    def write_data_into_single_file(self):
        try:
            # Define the output file name based on self.rule_type_name
            output_file_name = f"all_data_{self.rule_type_name}_rules.txt"
            # Construct the full path to the output file in the specified directory
            output_file_path = os.path.join(self.output_directory, output_file_name)
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                for filename in os.listdir(self.all_files_path):
                    new_file_name = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)
                    if new_file_name == f"{self.rule_type_name}_rules.txt":
                        file_path = os.path.join(self.all_files_path, filename)
                        with open(file_path, "r", encoding="utf-8") as input_file:
                            file_contents = input_file.read()
                            output_file.write(file_contents)
                output_file_path = output_file_path.replace('\\', '/')
                print(output_file_path)
            result_tar_bz2_path = RulesService.zip_specific_file(self.output_directory, self.zipped_path,
                                                                 output_file_name)
            return result_tar_bz2_path
        except Exception as e:
            print(e)

    @staticmethod
    def zip_specific_file(input_folder, output_folder, file_name):
        try:
            # Validate that the file exists in the input folder
            input_file_path = os.path.join(input_folder, file_name)
            if not os.path.exists(input_file_path):
                raise FileNotFoundError(
                    f"The specified file '{file_name}' does not exist in the folder '{input_folder}'.")
            file_name = file_name.replace('.txt', '')
            tar_bz2_name = f"{file_name}.zip"
            tar_bz2_path = os.path.join(output_folder, f"{file_name}.zip")
            tar_bz2_path = tar_bz2_path.replace('\\', '/')
            with zipfile.ZipFile(tar_bz2_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write(input_file_path, arcname=file_name)
            return tar_bz2_name
        except Exception as e:
            print(e)

    @staticmethod
    def rule_zipped_file(input_folder, output_folder, file_name, password, date_extracted, input_type):
        try:
            # Validate that the file exists in the input folder
            input_file_path = os.path.join(input_folder)
            if not os.path.exists(input_file_path):
                raise FileNotFoundError(
                    f"The specified file '{file_name}' does not exist in the folder '{input_folder}'.")
                # Create the date folder before calling the function
            date_folder_path = os.path.join(output_folder, date_extracted)
            date_folder_path = date_folder_path.replace('\\', '/')
            if not os.path.exists(date_folder_path):
                os.makedirs(date_folder_path)
            archived, archived_path = FetchedData.create_password_protected_archive(input_file_path, date_folder_path,
                                                                                    file_name, input_type, password)
            return archived, archived_path
        except Exception as e:
            print(e)
