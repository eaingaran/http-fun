from flask import Flask, request, jsonify, make_response
import re


app = Flask(__name__)


@app.route('/helloworld')
def hello_world():
    name = request.args.get('name')
    return 'Hello Stranger' if name is None else 'Hello ' + ' '.join(re.findall('[A-Z][^A-Z]*', name)), 200


@app.route('/versionz')
def version_info():
    info = {'git hash': '291250b2f59ce91f440c3261da3344192e6911c3', 'name': 'http-fun'}
    return jsonify(info), 200


@app.errorhandler(404)
def handle_404(e):
    return jsonify({'Status Code': 404, 'Message': str(e)}), 200


def say_hello():
    return 'Hello'


if __name__ == '__main__':
    print(say_hello())
