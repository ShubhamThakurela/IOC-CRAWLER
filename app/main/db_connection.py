from pymongo import MongoClient


class ConnectionService(object):
    """
    This class contains objects for Connections Strings to Mongodb
    :returns: All functions objects returns the Client and Connection of the Database
    """

    @staticmethod
    def db_collection_login():
        try:
            # MongoDB's connection settings
            #  Its using MongoClient to Connect with Host Url
            client = MongoClient('mongodb://localhost:27017/')
            # Defining the Server type
            db = client['local']
            # Creating the Collection as same as Mysql Database Table
            collection = db['login_db']
            return collection, client
        except Exception as q:
            print(q)

    @staticmethod
    def db_collection_source():
        try:
            # MongoDB's connection settings
            #  Its using MongoClient to Connect with Host Url
            client = MongoClient('mongodb://localhost:27017/')

            # Defining the Server type
            db = client['local']
            # Creating the Collection as same as Mysql Database Table
            collection = db['Sources_db']
            return collection, client
        except Exception as q:
            print(q)

    @staticmethod
    def db_collection_ip():
        try:
            # MongoDB's connection settings
            #  Its using MongoClient to Connect with Host Url
            client = MongoClient('mongodb://localhost:27017/')
            # Defining the Server type
            db = client['local']
            # Creating the Collection as same as Mysql Database Table
            collection = db['ip_db']
            return collection, client
        except Exception as q:
            print(q)

    @staticmethod
    def db_url_collection():
        try:
            # MongoDB's connection settings
            #  Its using MongoClient to Connect with Host Url
            client = MongoClient('mongodb://localhost:27017/')
            # Defining the Server type
            db = client['local']
            # Creating the Collection as same as Mysql Database Table
            collection = db['url_db']
            return collection, client
        except Exception as q:
            print(q)

    @staticmethod
    def db_domains_collection():
        try:
            # MongoDB's connection settings
            #  Its using MongoClient to Connect with Host Url
            client = MongoClient('mongodb://localhost:27017/')
            # Defining the Server type
            db = client['local']
            # Creating the Collection as same as Mysql Database Table
            collection = db['domains_db']
            return collection, client
        except Exception as q:
            print(q)

    @staticmethod
    def db_hashes_collection():
        try:
            # MongoDB's connection settings
            #  Its using MongoClient to Connect with Host Url
            client = MongoClient('mongodb://localhost:27017/')
            # Defining the Server type
            db = client['local']
            # Creating the Collection as same as Mysql Database Table
            collection = db['hashes_db']
            return collection, client
        except Exception as q:
            print(q)

    @staticmethod
    def db_subnet_collection():
        try:
            # MongoDB's connection settings
            #  Its using MongoClient to Connect with Host Url
            client = MongoClient('mongodb://localhost:27017/')
            # Defining the Server type
            db = client['local']
            # Creating the Collection as same as Mysql Database Table
            collection = db['subnet_db']
            return collection, client
        except Exception as q:
            print(q)
