__author__ = '4ikist'

from datetime import datetime, timedelta

from pymongo import mongo_client, ASCENDING

from properties import *


class DatabaseLogger(object):
    def __init__(self):
        client = mongo_client.MongoClient(host=db_host, port=db_port)
        self.rows = client['logging']['rows']
        self.rows.ensure_index('session_id', ASCENDING, unique=True)
        self.rows.ensure_index('leased_at', ASCENDING)

    def add_row(self, **kwargs):
        result = self.rows.save(kwargs)
        print result

    def modify_row(self, **kwargs):
        result = self.rows.update({'session_id': kwargs['session_id']}, {'$set': kwargs})
        print result


    def get_last(self):
        end = datetime.today()
        start = datetime.now() - timedelta(days=30)
        result = self.rows.find({'streaming_started_at': {'$gte': start, '$lt': end}}, {'_id':0}).sort('leased_at')
        return [el for el in result]


    def get_aggregated(self):
        self.rows.aggregate()


if __name__ == '__main__':
    pass
    