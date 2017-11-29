"""
Simple flask app
"""
import os
from flask import (Flask, request, redirect, url_for, send_from_directory,
                   flash, render_template)
import pandas as pd
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from testscript import test_function
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

@app.route('/', methods=['POST'])
def return_json_from_db():
    """
    Access the test table on postgres and return
    """

    values = request.get_json()
    print(str(values))
    strings = values.get('strings')
    if strings is None:
        return "Error: Please supply a valid string", 400

    # Get the database address from env vars

    db_string = os.getenv('DATABASE_URL')

    # Create connection

    engine = create_engine(db_string, echo=True)

    # Construct simple query

    query = f"SELECT * FROM test WHERE SOUNDEX(name) = SOUNDEX('{strings}')"

    # Run simple query on database
    
    data = pd.read_sql(query, engine)

    # Convert to a json

    response = data.to_json()

    # Return the json and a 200 (ok) response

    return response, 200

#def allowed_file(filename):
#    """
#    Check that the selected file is allowed
#
#    :param filename: <string> Filename of local file to be uploaded
#    :return: <boolean> True if filename is valid and extension is in
#     ALLOWED_EXTENSIONS, else False.
#    """
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Demonstrate an example of how to upload files to the server.

#@app.route('/upload', methods=['GET', 'POST'])
#def upload_file():
#    """
#    Upload a file using a simple form
#    """
#    if request.method == 'POST':
#        # check if the post request has the file part
#        if 'file' not in request.files:
#            flash(u'No file part', 'error')
#            return redirect(request.url)
#        selected_file = request.files['file']
#        # if user does not select file, browser also
#        # submit a empty part without filename
#        if selected_file.filename == '':
#            flash(u'No selected file', 'error')
#            return redirect(request.url)
#        if selected_file and not allowed_file(selected_file.filename):
#            flash(u'File is not of authorised type', 'error')
#            return redirect(request.url)
#        if selected_file and allowed_file(selected_file.filename):
#            filename = secure_filename(selected_file.filename)
#            selected_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            return redirect(url_for('uploaded_file',
#                                    filename=filename))
#    return render_template('upload.html')

# Render the file back to the user.

#@app.route('/data')
#def data():
#    """
#    Render uploaded file as a new webpage
#    """
#    db_string = os.getenv('DATABASE_URL')
#
#    # Create connection
#
#    engine = create_engine(db_string, echo=True)
#
#    # Construct simple query
#
#    query = f"SELECT * FROM test"
#
#    # Run simple query on database
#    
#    data = pd.read_sql(query, engine)
#
#    # Convert to a json
#
#    return str(data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
