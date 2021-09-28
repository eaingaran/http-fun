import argparse
import json
import os
import re
from datetime import datetime
import pytz
from logging.config import fileConfig


from flask import Flask, request, jsonify

app = Flask(__name__)


# validate the given argument to ensure it is an integer.
def numeric_val(val):
    if not val.isnumeric():
        raise argparse.ArgumentTypeError('Input Error. Expected a numeric value for duration. Found "{}"'
                                         .format(val))
    try:
        return int(val)
    except Exception as e:
        raise argparse.ArgumentTypeError("""Couldn't parse the value passed into integer. Value passed is "{}" """
                                         .format(val))


def log_requests(req, ts, status_code):
    app.logger.info(f'({req.method}) : {req.base_url} @ {ts} handled with status code {status_code}')
    app.logger.debug({'Timestamp': ts, 'Host': req.host.split(':')[0], 'Port': req.host.split(':')[1],
                      'Endpoint': req.base_url.replace(req.host_url, ''), 'Method': req.method, 'args': dict(req.args),
                      'data': req.data.decode('ascii'), 'ResponseCode': status_code})


@app.route('/helloworld')
def hello_world():
    curr_ts = datetime.now(pytz.utc)
    name = request.args.get('name')
    log_requests(request, curr_ts, 200)
    return 'Hello Stranger' if name is None else 'Hello ' + ' '.join(re.findall('[A-Z][^A-Z]*', name)), 200


@app.route('/versionz')
def version_info():
    curr_ts = datetime.now(pytz.utc)
    sha, name = 'Unable to find latest hash', 'Default Project Name'
    try:
        with open('config.ini', 'r') as config_file:
            config_json = json.load(config_file)
            sha, name = config_json['SHA'], config_json['ProjectName']
    except FileNotFoundError as e:
        print(f'Config file not found.', e)
    except Exception as e:
        print('Configurations could not be loaded', e)
    info = {'git hash': sha, 'name': name}
    log_requests(request, curr_ts, 200)
    return jsonify(info), 200


@app.errorhandler(404)
def handle_404(e):
    log_requests(request, datetime.now(pytz.utc), 404)
    return jsonify({'Status Code': 404, 'Message': str(e)}), 404


def say_hello():
    return 'Hello'


if __name__ == '__main__':
    fileConfig('logger.cfg')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, help='listening port for this application', type=numeric_val)
    parser.add_argument('-e', '--environment', default='dev', help='choose the environment ("dev", "prod")', type=str)
    args = parser.parse_args()

    override_port = os.environ.get('port')

    if override_port is None:
        override_port = args.port

    if args.environment == 'prod':
        from waitress import serve
        serve(app, host='0.0.0.0', port=override_port)
    else:
        app.run(host='0.0.0.0', port=override_port)
