import json
from flask import Flask, jsonify, request
import time
from threading import Thread

application = Flask(__name__)

main_route = '/flask-debug-server'

@application.route('/healthcheck')
def health_check():
    return jsonify(application='load-server',
                   status='OK',
                   build='N/A',
                   version='0.1',
                   NODE_ENV='python :)')


@application.route(main_route + '/debug', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def debug():
    sleep_in_ms = request.args.get('time')
    sleep_in_seconds = float(sleep_in_ms) / 1000
    Sleep(sleep_in_seconds).start()
    r_code = int(request.args.get('r_code'))
    response = jsonify(response_time=sleep_in_ms, request_method=request.method, response_code=r_code)
    response.status_code = r_code
    return response

@application.route(main_route + '/json_in_json_out', methods=['GET', 'POST'])
def json_in_json_out():
    if request.method == 'POST':
        try:
            json_data = json.loads(request.data)
            return jsonify(response=json_data)
        except:
            return error_handler('Unable to parse json')

@application.route(main_route + '/')
def root():
    endpoints = {'debug': '/debug{?r_code,time*}', 'healthcheck': '/healthcheck'}
    return jsonify(supported_endpoints=endpoints, success=True)


def error_handler(message):
    return jsonify(error_message=message, success=False)


class Sleep(Thread):
    def __init__(self, sleep_in_seconds):
        super(Sleep, self).__init__()
        time.sleep(sleep_in_seconds)

if __name__ == '__main__':
    # application.run(port=8080, debug=True)
    application.run('0.0.0.0')