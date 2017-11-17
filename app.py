"""
Simple flask app
"""
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
print('Hello World')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
