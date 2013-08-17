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
        return result

    def modify_row(self, **kwargs):
        result = self.rows.update({'session_id': kwargs['session_id']}, {'$set': kwargs})
        return result


    def get_last(self):
        today = datetime.today()
        end = datetime(today.year, today.month, today.day) + timedelta(days=1)
        start = end - timedelta(days=30)

        result = self.rows.find({'streaming_started_at': {'$gte': start, '$lte': end}}, {'_id': 0}).sort('leased_at')
        return [el for el in result]


    def get_aggregated(self):
        result = []
        today = datetime.today()
        global_start = datetime(today.year, today.month, today.day) + timedelta(days=1)
        for i in range(0, 30, 1):
            end = global_start - timedelta(days=i)
            start = global_start - timedelta(days=i + 1)
            day_result = {'day': start}
            day_result_sessions = self.rows.find({'streaming_started_at': {'$gt': start, '$lte': end}}, {'_id': 0})

            unique_count = set()
            status_crash = 0
            status_ok = 0
            ticket_not_null = 0
            all_length_session = 0
            for el in day_result_sessions:
                unique_count.add(el['identity'])
                if el['status'] == 'crash':
                    status_crash += 1
                if el['status'] == 'ok':
                    status_ok += 1
                if el['ticket'] is not None:
                    ticket_not_null += 1
                all_length_session += el['duration']

            day_result['sessions_count'] = day_result_sessions.count()
            day_result['median_length_of_session'] = float(all_length_session) / day_result['sessions_count'] if \
                day_result['sessions_count'] != 0 else 0
            day_result['unique_count'] = len(unique_count)
            day_result['crash_status_count'] = status_crash
            day_result['ok_status_count'] = status_ok
            day_result['not_null_ticket_count'] = ticket_not_null
            result.append(day_result)
        return result


if __name__ == '__main__':
    pass
    