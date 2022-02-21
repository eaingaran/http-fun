import argparse
import json
import os
import pathlib
import re
from datetime import datetime
from logging.config import fileConfig
from os import path
import requests
import socket

import pytz
from flask import Flask, request, jsonify

app_config = None


def get_config(key):
    global app_config
    if app_config is None:
        base_dir = pathlib.Path(__file__).parent.resolve()
        try:
            with open(path.join(base_dir, 'config.ini'), 'r') as config_file:
                app_config = json.load(config_file)
        except FileNotFoundError as e:
            print(f'Config file not found.', e)
        except Exception as e:
            print('Configurations could not be loaded', e)
    return app_config[key] if key in app_config else ''


app_name = get_config('ProjectName')
app = Flask(app_name)


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
    app.logger.debug({'Timestamp': ts, 'Host': req.host.split(':')[0],
                      'Port': req.host.split(':')[1] if req.host.__contains__(':') else 0,
                      'Endpoint': req.base_url.replace(req.host_url, ''), 'Method': req.method, 'args': dict(req.args),
                      'data': req.data.decode('ascii'), 'ResponseCode': status_code})


@app.route("/healthcheck")
def health_check():
    return jsonify({"pong": True}), 200


@app.route('/helloworld')
def hello_world():
    curr_ts = datetime.now(pytz.utc)
    name = request.args.get('name')
    log_requests(request, curr_ts, 200)
    return 'Hello Stranger' if name is None else 'Hello ' + ' '.join(re.findall('[A-Z][^A-Z]*', name)), 200


@app.route('/versionz')
def version_info():
    curr_ts = datetime.now(pytz.utc)
    info = {'git hash': get_config('SHA'), 'name': get_config('ProjectName'),
            'image version': 'v1.73', 'hostname': socket.gethostname()}
    log_requests(request, curr_ts, 200)
    return jsonify(info), 200


@app.errorhandler(404)
def handle_404(e):
    log_requests(request, datetime.now(pytz.utc), 404)
    return jsonify({'Status Code': 404, 'Message': str(e)}), 404


@app.route('/destroy')
def destroy_app():
    shutdown_sequence = request.environ.get('werkzeug.server.shutdown')
    if shutdown_sequence is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_sequence()
    return 'Shutdown initiated...'


@app.route('/redirect')
def redirect():
    curr_ts = datetime.now(pytz.utc)
    app.logger.info('Redirect request received...')
    re_host = request.args.get('host')
    re_route = request.args.get('route')
    log_requests(request, curr_ts, 200)
    app.logger.info(f'Trying to get response from http://{re_host}/{re_route}')
    try:
        return requests.get(f"http://{re_host}/{re_route}", timeout=60).content
    except Exception as e:
        return jsonify({'Status Code': 400, 'Message': str(e)}), 400


def start_app(host, port, environment):
    if environment == 'prod':
        from waitress import serve
        serve(app, host=host, port=port)
    else:
        app.run(host=host, port=port)


if __name__ == '__main__':
    fileConfig('logger.cfg')

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, help='listening port for this application', type=numeric_val)
    parser.add_argument('-e', '--environment', default='dev', help='choose the environment ("dev", "prod")', type=str)
    args = parser.parse_args()

    override_port = os.environ.get('port')

    if override_port is None:
        override_port = args.port

    start_app('0.0.0.0', override_port, args.environment)

# http://${consumer_service_external_ip}/versionz
# http://${consumer_service_external_ip}/redirect?host=http-fun-pro-service.prod.svc.clusterset.local:5000&route=versionz
