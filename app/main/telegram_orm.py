import pymongo
from datetime import datetime, timedelta


class DbOrmTelegram:
    @staticmethod
    def run_queries_fetched_result(input_type, after_time, before_time):
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017")
            db = client["telegram_scraper"]
            tele_collection = db["posts"]
            # Parse the string into a datetime object
            date_format = "%Y-%m-%d"
            after_date = datetime.strptime(after_time, date_format).date()
            before_date = datetime.strptime(before_time, date_format).date()
            # Convert to Unix timestamps
            unix_after_time = int(datetime(after_date.year, after_date.month, after_date.day).timestamp())
            unix_before_time = int(datetime(before_date.year, before_date.month, before_date.day).timestamp())
            filters_criteria = {
                "channel": input_type,
                "$and": [{"time": {"$lte": unix_after_time}}, {"time": {"$gte": unix_before_time}}],
            }
            # filters_criteria = {
            #     "channel": input_type,
            # }
            result = tele_collection.find(filters_criteria)
            if result:
                return result
        except Exception as e:
            print(e)
