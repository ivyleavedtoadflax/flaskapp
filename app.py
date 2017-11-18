"""
Simple flask app
"""
import os
from flask import (Flask, request, redirect, url_for, send_from_directory,
        flash)
import pandas as pd
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the location where uploaded files will be stored (/tmp/ is probably ok)
# Note that at present these will remain on the server until it is rebooted.

UPLOAD_FOLDER = '/tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the app secret key to prevent CSRF

app.secret_key = os.urandom(24)

# Which extensions are allowed to be uploaded?

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'json'])

# Demonstrate access to an attached database using sqlalchemy and pandas

@app.route('/', methods=['GET'])
def return_json_from_db():
    """
    Access the test table on postgres and return
    """

    # Get the database address from env vars

    db_string = os.getenv('DATABASE_URL')

    # Create connection

    ENGINE = create_engine(db_string, echo=True)

    # Run simple query on database

    data = pd.read_sql('SELECT * FROM test', ENGINE)

    # Convert to a json

    response = data.to_json()

    # Return the json and a 200 (ok) response
    
    return response, 200

def allowed_file(filename):
    """
    Check that the selected file is allowed

    :param filename: <string> Filename of local file to be uploaded 
    :return: <boolean> True if filename is valid and extension is in 
    ALLOWED_EXTENSIONS, else False.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Demonstrate an example of how to upload files to the server.

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and not allowed_file(file.filename):
            flash('File is not of authorised type')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <h2>Accepts csv, json, or txt files only.</h2>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# Render the file back to the user.

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
