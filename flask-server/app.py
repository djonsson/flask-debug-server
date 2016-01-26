from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/healthcheck')
def health_check():
    return jsonify(application='load-server',
                   status='OK',
                   build='N/A',
                   version='0.1',
                   NODE_ENV='python :)')


@app.route('/debug', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def debug():
    sleep_in_ms = time_to_wait()
    r_code = int(request.args.get('r_code'))
    response = jsonify(response_time=sleep_in_ms, request_method=request.method, response_code=r_code)
    response.status_code = r_code
    return response


def time_to_wait():
    sleep_in_ms = request.args.get('time')
    sleep_in_seconds = float(sleep_in_ms) / 1000
    time.sleep(sleep_in_seconds)
    return float(sleep_in_ms)


@app.route('/')
def root():
    endpoints = {'debug': '/debug{?r_code,time*}', 'healthcheck': '/healthcheck'}
    return jsonify(supported_endpoints=endpoints)


if __name__ == '__main__':
#    app.run(port=8080, debug=True)
    app.run('0.0.0.0')