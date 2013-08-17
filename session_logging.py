#coding: utf-8
from datetime import datetime, timedelta

from flask import Flask, request, redirect, url_for, render_template, make_response, json

import db_manager
from properties import *


app = Flask(__name__)

db_client = db_manager.DatabaseLogger()


@app.route('/')
def main():
    return redirect(url_for('session_process'))


def format_datetime(string_datetime):
    try:
        offset = int(string_datetime[-5:])
    except:
        return datetime.strptime(string_datetime, date_format)

    delta = timedelta(hours=offset / 100)
    time = datetime.strptime(string_datetime[:-6], date_format)
    time -= delta
    return time


def validate_session_params(params):
    result = {}
    try:
        result['session_id'] = int(params['session_id'])
        result['app_name'] = params['app_name']
        result['identity'] = params['identity']
        result['identity_type'] = params['identity_type']
        result['status'] = params['status']
        result['ticket'] = params['ticket'] if params['ticket'] != 'null' else None
        result['duration'] = int(params['duration'])
        result['leased_at'] = format_datetime(params['leased_at'])
        result['streaming_started_at'] = format_datetime(params['streaming_started_at'])
        result['latency'] = int(params['latency'])
        result['bytes_sent'] = int(params['bytes_sent'])
        return result
    except Exception as e:
        return None


def add_session_params(params, function=db_client.add_row):
    session_params = validate_session_params(params)
    if session_params:
        try:
            result = function(**session_params)
            return make_response(json.dumps({'success': True, 'detail': str(result)}))
        except Exception as e:
            return make_response(json.dumps({'success': False, 'error': str(e)}))
    else:
        return make_response(json.dumps({'success': False, 'error': 'Bad params'}))


@app.route('/sessions', methods=['POST', 'GET', 'PUT'])
def session_process():
    if request.method == 'POST':
        return add_session_params(request.form, db_client.add_row)

    if request.method == 'PUT':
        return add_session_params(request.form, db_client.modify_row)

    if request.method == 'GET':
        sessions = db_client.get_last()
        if len(sessions):
            session_keys = sessions[0].keys()
            return render_template('last_sessions.html', sessions=sessions, session_keys=session_keys)
        return make_response(json.dumps({'success': True, 'error': 'no sessions by this dates'}))

    return make_response(json.dumps({'success': False, 'error': 'unrecognized method'}))


@app.route('/sessions/report')
def sessions_aggregate():
    aggregated = db_client.get_aggregated()
    return render_template('report.html', reports=aggregated)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
