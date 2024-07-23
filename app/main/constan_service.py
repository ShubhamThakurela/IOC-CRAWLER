import datetime
import time
import pandas as pd
import os
from .paths import IN_PATH, KEYFILE_PATH, SCRAPPED_PATH, FILE_CONFIG_PATH, LOG_PATH, PROCESSED_PATH, CHROME_PATH, \
    SERVER_HOST, LATEST_PATH, RULES_PATH
from .ioc_utils import extract_name_from_url


class ConstantService:
    """
    This class is for Constant paths, browsers, logs, mails, for keeping them in to folders also using in application
    """

    @staticmethod
    def fetched_scraped_data():
        """
        :return: The paths of Folders
        """
        time.sleep(3)
        # return paths.SCRAPPED_PATH + '/' + datetime.datetime.utctime(datetime.datetime.now(), '%Y%m%d')
        return SCRAPPED_PATH + '/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

    @staticmethod
    def get_configure_file():
        file_path = FILE_CONFIG_PATH
        excel_files = [f for f in os.listdir(file_path) if f.endswith('.xlsx')]
        if not excel_files:
            raise FileNotFoundError("No Excel files found in the directory.")
        # Assuming you want to pick the latest modified file
        latest_excel_file = max(excel_files, key=lambda f: os.path.getmtime(os.path.join(file_path, f)))
        file_path_1 = os.path.join(file_path, latest_excel_file)
        df = pd.read_excel(file_path_1)
        url_list = list(df['domains_white_list'])
        all_domain = []
        for url_1 in url_list:
            if 'nan' in url_1:
                pass
            else:
                domain_name = extract_name_from_url(url_1)
                all_domain.append(domain_name)
        return all_domain

    @staticmethod
    def data_in_path():
        return IN_PATH

    @staticmethod
    def data_processed_path():
        return PROCESSED_PATH

    @staticmethod
    def data_latest_path():
        return LATEST_PATH

    @staticmethod
    def data_out_path():
        return SCRAPPED_PATH

    @staticmethod
    def log_path():
        return LOG_PATH

    @staticmethod
    def rules_data_out_path():
        return RULES_PATH

    @staticmethod
    def server_host():
        return SERVER_HOST

    @staticmethod
    def get_chrome_path():
        return CHROME_PATH

    @staticmethod
    def get_user_agent():
        """
        :return:  the User Agent for request
        """
        # return proxy.ua.random
        return 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'

    @staticmethod
    def cc_mail_id():
        return ""

    @staticmethod
    def get_all_search_engines():
        return [
            'google.com',
            'yahoo.com',
            'bing.com',
            'duckduckgo.com',
            'ask.com',

        ]
