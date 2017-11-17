"""
Simple flask app
"""
import os
from flask import Flask
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

    # Convert to string and return
    
    return str(data)

@app.route('/foo', methods=['GET'])
def hello1():
    return "Hello!"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
