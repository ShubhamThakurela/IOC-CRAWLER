import ipaddress
import json
import os
import re
import time
import zipfile
from datetime import datetime
import pandas as pd
import requests
# import app.main.proxy as proxy
from .ioc_orm import IocOrm, DbOrmIoc
from .constan_service import ConstantService
from .ioc_utils import ProcessAllIoc
from typing import Optional
from .ioc_utils import extract_name_from_url
from bson import Binary
from bson import json_util
import binascii
from .latest_ioc_orm import MonitorOrm


# from .ioc_orm import DbOrmIoc


class IocService(object):
    # Function to extract all type and insert into db
    @staticmethod
    def crawl_all_ioc(url: Optional[str] = None, ioc_type: Optional[list] = None):
        """
        :param ioc_type: ioc types string value ...
        :param url: URL from which the data needs to be extract
        :return: Its returns the status of the IOC extraction function also returns the Exceptions (String)
        """
        try:
            # Initialized the raw_data as None for handling the errors exceptions
            raw_data = None
            #  Calling the user defined function object to get the url content in raw_data
            raw_data = request_data(url)
            # collecting lists from input excel
            all_domains_list = ConstantService.get_configure_file()
            # condition to check if raw_data is None.
            if not isinstance(raw_data, type(None)):
                data_extraction_object = ProcessAllIoc(raw_data, url, all_domains_list, ioc_type)
                results_of_extraction = data_extraction_object.extract_all_ioc()
                # checking the length of the list_dict.....
                if results_of_extraction:
                    return results_of_extraction
            else:
                return "EMPTY_DATA", 403,
        except Exception as k:
            print(k)

    @staticmethod
    def crawl_by_file(file_path):
        """ This function returns the status of execution as a report,
        :param file_path: its fetched location of the parsed file
        :return: returns Result or Exception (String) """
        report = None
        try:
            # Initialized the Counter for Monitoring the processing urls.
            counter = 1
            raw_data = None
            source = None
            source_list = []
            # Calling the (get_configure_xlsx) Reading the Excel file into the dataframe and parsing forward
            # Iteration through the index and row of the dataframe to read Each url and Ioc_type of the url
            # Converting Excel into Dataframe
            data_frame = pd.read_excel(file_path)
            url_list = data_frame['urls'].tolist()
            ioc_type_list = data_frame['type'].tolist()
            data_extraction_type = data_frame['data_extraction_type'].tolist()
            # Loop through both lists simultaneously using zip()
            for url, ioc_type, ext_type in zip(url_list, ioc_type_list, data_extraction_type):
                raw_data = request_data(url)
                if not pd.notna(url):  # Assuming pandas is imported and nan values are represented by 'nan'
                    break
                if not isinstance(raw_data, type(None)):
                    pass
                    # printing the live url with counter to the console and its type to monitor.
                    print(str(counter) + "- Data Processing Begins-" + str(url) + " ," + "Ioc_type =" + str(ioc_type))
                    # function calling (crawl_by_url)m to extract the desired data.
                    if data_extraction_type == 'no':
                        source = extract_name_from_url(url)
                        status = IocService.crawl_all_ioc(url, ioc_type)
                        # Printing the workflow processed with report (string) as a result
                        print(str(counter) + "- Data Processed-" + str(url) + "," + "report =" + str(status))
                        # Counter increment for continue lopping
                        source_url_dict = {
                            "Url": url.strip(),
                            "last_extraction_time": datetime.now().strftime("%Y-%m-%d"),
                            "source": source,
                            "source_type": ioc_type,
                        }
                        source_list.append(source_url_dict)
                        counter += 1
                    else:
                        # raw_data = request_data(url)
                        if not isinstance(raw_data, type(None)):
                            pass
                            source = extract_name_from_url(url)
                            source_url_dict = {
                                "Url": url.strip(),
                                "last_extraction_time": datetime.now().strftime("%Y-%m-%d"),
                                "source": source,
                                "source_type": ioc_type,
                            }
                            if ioc_type == 'ip':
                                # Main Data Extraction Function object processing_ip called to extract the ips and
                                # inserting into db
                                ips_object = ProcessingData(raw_data, url, ioc_type)
                                status = ips_object.processing_ips()
                            elif ioc_type == 'url':
                                url_object = ProcessingData(raw_data, url, ioc_type)
                                status = url_object.processing_urls()
                            elif ioc_type == 'hashes':
                                hashes_obj = ProcessingData(raw_data, url, ioc_type)
                                status = hashes_obj.processing_hashes()
                            elif ioc_type == 'domain':
                                domain_obj = ProcessingData(raw_data, url, ioc_type)
                                status = domain_obj.processing_domains()
                            elif ioc_type == 'subnet':
                                subnet_obj = ProcessingData(raw_data, url, ioc_type)
                                status = subnet_obj.processing_subnet()
                            source_list.append(source_url_dict)
                            # source_insrt_obj = IocOrm(source_list)
                            # dict_source_insertion = source_insrt_obj.insert_sources()
                            print(str(counter) + "- Data Processed-" + str(url) + "," + "report =" + str(status))
                            counter += 1
            source_insrt_obj = IocOrm(source_list)
            dict_source_insertion = source_insrt_obj.insert_sources()
            return "True"
        except Exception as e:
            print(e)
            return str(e)

    @staticmethod
    def crawl_single_ioc_url(url: Optional[str] = None, ioc_type: Optional[list] or [str] = None, ):
        """
        :param url: RL from which the data needs to be extract
        :param ioc_type:  like ip, hash, domain, url, its use to check the typ of url and
         send to the right functionality
        :return: Its returns the status of the IOC extraction function also returns the Exceptions (String)
        """
        try:
            sources_dict = {}
            source_url_dt_list = []
            # Initialized the raw_data as None for handling the errors exceptions
            raw_data = None
            #  Calling the user defined function object to get the url content in raw_data
            raw_data = request_data(url)
            source = extract_name_from_url(url)
            sources_dict.update({"Url": url.strip(),
                                 "extraction_date": datetime.now(),
                                 "source": source,
                                 "source_type": ioc_type})
            # condition to check if raw_data is None.
            if not isinstance(raw_data, type(None)):
                source_url_dt_list.append(sources_dict)
                if ioc_type == 'ip':
                    # Main Data Extraction Function object processing_ip called to extract the ips and inserting into db
                    ips_object = ProcessingData(raw_data, url, ioc_type)
                    status = ips_object.processing_ips()
                    return status
                elif ioc_type == 'url':
                    url_object = ProcessingData(raw_data, url, ioc_type)
                    status = url_object.processing_urls()
                    return status
                elif ioc_type == 'hashes':
                    hashes_obj = ProcessingData(raw_data, url, ioc_type)
                    status = hashes_obj.processing_hashes()
                    return status
                elif ioc_type == 'domain':
                    domain_obj = ProcessingData(raw_data, url, ioc_type)
                    status = domain_obj.processing_domains()
                    return status
                elif ioc_type == 'subnet':
                    subnet_obj = ProcessingData(raw_data, url, ioc_type)
                    status = subnet_obj.processing_subnet()
                    return status
                source_insrt_obj = IocOrm(source_url_dt_list)
                dict_source_insertion = source_insrt_obj.insert_sources()
                if dict_source_insertion:
                    return True
                else:
                    return "Ioc not found"
            else:
                return "EMPTY_DATA", 403

        except Exception as e:
            print(e)
            return "EXCEPTION", 403


# class and has 5 members Ioc processing ips, urls, domains, hash, subnet interdependently.
class ProcessingData:
    def __init__(self, raw_data, url, ioc_type):
        self.raw_data = raw_data
        self.url = url
        self.source_url_type = ioc_type

    def processing_subnet(self):
        """
        param self.raw_data The Raw data of Url
        :param self.url In which data extracted
        :return: Exception Strings
        """
        data_list = []
        try:
            subnet_pattern = (r"\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]["
                              r"0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]["
                              r"0-9]?)\/\d{1,2}\b")
            matched_lines = find_subnets(subnet_pattern, self.raw_data)
            for line in matched_lines:
                current_datetime = datetime.now().strftime("%Y-%m-%d")
                subnet_matches = line
                ip_address, subnet_cidr_notation = subnet_notation(line)
                ipadress_type = check_ip_type(ip_address)
                data_d = {"subnet": subnet_matches,
                          "subnet_cidr_notation": subnet_cidr_notation,
                          "subnet_ip_type": ipadress_type,
                          'source_url': self.url,
                          "source_type": self.source_url_type,
                          'first_timestamp': current_datetime, 'ref_domain': None,
                          'ref_hashes': None, 'ref_ips': None
                          }
                # Remove key-value pairs where the value is None
                filtered_data = {key: value for key, value in data_d.items() if value is not None}
                data_list.append(filtered_data)
            data_insertion_obj = IocOrm(data_list)
            results = data_insertion_obj.insert_data()
            return "True"
        except Exception as a:
            print(a)
            return "EXCEPTION_OCCURRED"

    def processing_ips(self):
        """
        It takes the raw_data and apply the regex for extraction available Ips inside the raw_data
        :param self.url Source url in which data being extracted
        :param self.raw_data raw_data of hashes as a List
        :return:1.Exception (string) it through the error and pass the execution whenever there is no data matched.
        """
        ip_type = None
        data_list = []
        try:
            # Hard Coded Patters for Ips
            ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
            ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
            ipv6_pattern = r'^(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}$'
            # Splitting the raw_data into lines for loop through all the lines
            lines = self.raw_data.split('\n')
            for line in lines:
                current_datetime = datetime.now().strftime("%Y-%m-%d")
                ip_matches = re.findall(ip_pattern, line)
                for ip in ip_matches:
                    # conditions to check the type of ip
                    if re.match(ipv4_pattern, ip):
                        ip_type = "IPv4 address"
                    elif re.match(ipv6_pattern, ip):
                        ip_type = "IPv6 address"
                    # Defining the keys of dict and assigning the values to it.
                    data_d = {'ip': ip, 'ip_type': ip_type, 'source_url': self.url,
                              "source_type": [self.source_url_type],
                              'first_timestamp': current_datetime, 'ref_domain': None, 'ref_hashes': None,
                              'ref_urls': None}
                    # Remove key-value pairs where the value is None
                    filtered_data = {key: value for key, value in data_d.items() if value is not None}
                    data_list.append(filtered_data)
                    # # Appending Each dict into Single list....
                    # data_list.append(data_d)
            # Calling the IOC ORM for data insertion operations ORM LAYER
            data_insertion_obj = IocOrm(data_list)
            results = data_insertion_obj.insert_data()
            return "True"
        except Exception as e:
            print(e)
            return "EXCEPTION_OCCURRED"

    def processing_urls(self):
        """
        param self.raw_data The Raw data of Url
        :param self.url In which data extracted
        :return: Exception Strings
        """
        data_list = []
        try:
            url_pattern = r'https?://[^,]+'
            protocol_pattern = r"^https?://"
            # list to store dictionaries
            lines = self.raw_data.split('\n')
            for line in lines[9:]:
                current_datetime = datetime.now().strftime("%Y-%m-%d")
                url_matches = re.search(url_pattern, line)
                if url_matches:
                    mach_text = url_matches.group(0)
                    mach_text = mach_text.replace('"', '')
                    if re.match(protocol_pattern, mach_text):
                        type_url = "http"
                    else:
                        type_url = "https"
                    data_d = {'url': mach_text, 'url_type': type_url, 'source_url': self.url,
                              "source_type": [self.source_url_type], 'first_timestamp': current_datetime,
                              'ref_domain': None,
                              'ref_hashes': None, 'ref_ips': None}
                    # Remove key-value pairs where the value is None
                    filtered_data = {key: value for key, value in data_d.items() if value is not None}
                    data_list.append(filtered_data)
                    # data_list.append(data_d)
            data_insertion_obj = IocOrm(data_list)
            results = data_insertion_obj.insert_data()
            return "True"
        except Exception as a:
            print(a)
            return "EXCEPTION_OCCURRED"

    def processing_domains(self):
        """
        :param self: URl and Raw_data
        :return: Exception String when error occurred
        """
        raw_data = self.raw_data
        url = self.url
        try:
            data_list = []
            # Define the regex pattern for domain extraction
            domains_pattern = r'(?:[a-z]+\.)+[a-z]+\.[a-z]+'
            tld_pattern = r"(\.[a-z]+)$"
            # Initialize a list to store dictionaries
            # Extract IPs and URLs using regex and create a dictionary for each IP
            lines = raw_data.split('\n')
            for line in lines:
                current_datetime = datetime.now().strftime("%Y-%m-%d")
                url_matches = re.findall(domains_pattern, line)
                for domain in url_matches:
                    domain_type = re.search(tld_pattern, domain)
                    mach_text = domain_type.group(0)
                    data_d = {'domain': domain, 'domain_type': mach_text, 'source_url': url,
                              "source_type": [self.source_url_type], 'first_timestamp': current_datetime,
                              'ref_urls': None, 'ref_hashes': None, 'ref_ips': None}
                    # Remove key-value pairs where the value is None
                    filtered_data = {key: value for key, value in data_d.items() if value is not None}
                    data_list.append(filtered_data)
                    # data_list.append(data_d)
            insertion_obj = IocOrm(data_list)
            results = insertion_obj.insert_data()
            return results
        except Exception as a:
            print(a)
            return "EXCEPTION_OCCURRED"

    def processing_hashes(self):
        """
        :return: Exception (string) it through the error and pass the execution whenever there is no data matched.
        """
        data_list = []
        try:
            raw_data = self.raw_data
            # Calling the Find_hashes function from outside the class
            hashes = find_hashes(raw_data)
            # looping Through the union list to extract hash from each line
            for line in hashes:
                current_datetime = datetime.now().strftime("%Y-%m-%d")
                # Condition checking based on len of line to get the hash types.
                if len(line) == 32:
                    hash_type = 'MD5'
                elif len(line) == 40:
                    hash_type = 'SHA1'
                elif len(line) == 64:
                    hash_type = 'SHA256'
                else:
                    hash_type = 'Invalid'
                    # Data dict creation....
                data_d = {'hash': line, 'hash_type': hash_type, 'source_url': self.url,
                          "source_type": [self.source_url_type], 'first_timestamp': current_datetime,
                          'ref_domain': None, 'ref_urls': None, 'ref_ips': None}
                # Remove key-value pairs where the value is None
                filtered_data = {key: value for key, value in data_d.items() if value is not None}
                data_list.append(filtered_data)
                # data_list.append(data_d)
            data_insertion_obj = IocOrm(data_list)
            results = data_insertion_obj.insert_data()
            return data_list, results
        except Exception as a:
            print(a)
            return "EXCEPTION_OCCURRED"


class FetchedData:

    @staticmethod
    def fetch_only_sources(source_type):
        try:
            result_list = []
            fetched_result = DbOrmIoc.source_queries_fetched_result(source_type)
            if fetched_result:
                for item in fetched_result:
                    if "_id" in item:
                        del item["_id"]
                        result_list.append(item)
                return result_list
            else:
                db_result = "No Document found!, Try again"
                return "no results"
        except Exception as e:
            print(e)

    @staticmethod
    def fetch_all_collections(source_type, file_path, zipped_path):
        try:
            ioc_type = source_type
            date_extracted = time.strftime("%Y-%m-%d")
            fetched_results = DbOrmIoc.run_queries_fetched_result(source_type, date_extracted)
            fetched_results = list(fetched_results)
            if fetched_results:
                date_time_obj = time.strftime("%Y-%m-%d")
                # Create the filename by concatenating date_time_obj and ioc_type
                filename = f"{date_time_obj}-{ioc_type}.txt"
                file_path = file_path.replace('\\', '/')
                # Write the custom line at the beginning of the file
                with open(file_path + '/' + filename, 'w') as file:
                    # Loop through the documents and write them to the file
                    for document in reversed(fetched_results):
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
                                        print(value_at_index_2)
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
                                    print(value_at_index_2)
                                    # Write the first key-value pair as a JSON object to the file
                                    file.write(json.dumps(value_at_index_2) + '\n')
                resulting_tar_bz2_path = FetchedData.zip_specific_file(file_path, zipped_path, filename)
                return resulting_tar_bz2_path
            else:
                db_result = "No Document found!, Try again"
                return "no results"
        except Exception as e:
            return e

    @staticmethod
    def fetch_by_params(source_type, file_path, zipped_path, date_extracted):
        try:
            ioc_type = source_type
            fetched_results = MonitorOrm.run_queries_fetched_result(source_type, date_extracted)
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
                                        print(value_at_index_2)
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
                                    print(value_at_index_2)
                                    # Write the first key-value pair as a JSON object to the file
                                    file.write(json.dumps(value_at_index_2) + '\n')
                resulting_zipped_path = FetchedData.zip_specific_file(file_path, zipped_path, filename)
                return resulting_zipped_path
            else:
                db_result = "No Document found!, Try again"
                return "no results"
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
    def zip_specific_file(input_folder, output_folder, file_name):
        try:
            # Validate that the file exists in the input folder
            input_file_path = os.path.join(input_folder, file_name)
            if not os.path.exists(input_file_path):
                raise FileNotFoundError(
                    f"The specified file '{file_name}' does not exist in the folder '{input_folder}'.")
            # file_name = file_name.replace('.txt', '')
            zip_name = file_name.replace('.txt', '')
            tar_bz2_name = f"{zip_name}.zip"
            tar_bz2_path = os.path.join(output_folder, f"{zip_name}.zip")
            tar_bz2_path = tar_bz2_path.replace('\\', '/')
            with zipfile.ZipFile(tar_bz2_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write(input_file_path, arcname=file_name)
            return tar_bz2_name
        except Exception as e:
            print(e)


def request_data(page_url: Optional[str] = None) -> Optional[str]:
    """
    It fetches the data from the requested url and gives a response in the format of string.
    :param page_url: URL from which the data needs to be extracted
    :return: String of Text Data or None
    """
    # # Get Random User Agent String.
    # referer = random.choice(ConstantService.get_all_search_engines())
    # # It sets a proxy header and a referrer
    # headers = {'User-Agent': proxy.ua.random, 'Referer': referer, 'Accept-Language': 'en-US,en;q=0.5'}
    try:
        # # The code fetches the data using get request
        # response = requests.get(page_url, headers=headers, timeout=30, allow_redirects=True)
        response = requests.get(page_url)
        time.sleep(3)
        status_code = response.status_code
        # checks for status_code 200 to return the response
        if status_code == 200:
            return response.text
        else:
            return None
        # Prints Exception and return None if it
    except Exception as e:
        print(repr(e))
        return None


def find_hashes(raw_data: Optional[str] = None):
    """
    It takes the raw_data and apply the regex for extracting available Hashes MD5, SHA1, SHA256 inside the raw_data,
    :param raw_data: raw_data of hashes as a List
    :return:1.Exception (string) it through the error and pass the execution whenever there is no data in raw_data
    :return:2. Return the Matched hash    """
    try:
        # Regular expression pattern to match MD5, SHA1, and SHA256 hashes
        pattern = r"\b(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\b"
        # Use regex findall to extract all hash occurrences
        hashes = re.findall(pattern, raw_data)
        return hashes
    except Exception as i:
        print(repr(i))
        return repr(i)


def find_subnets(subnet_pattern, raw_data):
    try:
        pattern = subnet_pattern
        subnets = re.findall(pattern, raw_data)
        return subnets
    except Exception as e:
        print(repr(e))
        return repr(e)


def subnet_notation(subnet):
    subnet_string = str(subnet)
    # Split the string by "/"
    ip_address, prefix_length_str = subnet_string.split("/")
    # Convert the prefix length to an integer
    prefix_length = int(prefix_length_str)
    return ip_address, prefix_length


def check_ip_type(ip_address):
    try:
        # Try to create an IP address object
        ip = ipaddress.ip_address(ip_address)

        # Check if it's an IPv4 address
        if isinstance(ip, ipaddress.IPv4Address):
            return "IPv4"
        # Check if it's an IPv6 address
        elif isinstance(ip, ipaddress.IPv6Address):
            return "IPv6"
        else:
            return "Unknown"
    except ValueError:
        # If the IP address is invalid, ValueError will be raised
        return "IP not Given"
