from flask import Flask, request, jsonify
import re


app = Flask(__name__)


@app.route('/helloworld')
def hello_world():
    name = request.args.get('name')
    return 'Hello Stranger' if name is None else 'Hello ' + ' '.join(re.findall('[A-Z][^A-Z]*', name))


def say_hello():
    return 'Hello'


if __name__ == '__main__':
    print(say_hello())
