"""
Simple flask app
"""
import os
from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# Set up a route for the base url

@app.route('/', methods=['GET'])
def hello():

    # Get the database address from env vars

    db_string = os.getenv('DATABASE_URL')

    # Create connection

    ENGINE = create_engine(db_string, echo=True)

    # Run simple query on database

    data = pd.read_sql('SELECT * FROM user', ENGINE)

    # Convert to a json

    response = data.to_json()

    # Return the json and a 200 (ok) response
    
    return response, 200

@app.route('/foo', methods=['GET'])
def hello1():
    return "Hello!"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
