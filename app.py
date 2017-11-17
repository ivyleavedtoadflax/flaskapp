"""
Simple flask app
"""
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/foo', methods=['GET'])
def hello1():
    return "Hello!"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
