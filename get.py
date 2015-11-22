#!/usr/bin/python3
# -*- coding: utf-8 -*-

""""
Author:  Jan Harasym <jharasym@linux.com>
Website: dijit.sh

Creation Date: 2015-10-22
Last Modified: Sun 22 Nov 23:47:06 2015

Description:
Expected Use:
"""

from flask import Flask, request, redirect, url_for, render_template, make_response, abort
import json
import glob
import redis
from hashlib import sha256
import os

app = Flask(__name__)
dbconn = redis.Redis()

def redis_set(hash,image):
    try:
        db = redis.Redis()
        db.setex(hash,image,1000)
        # FIXME: Hardcoded mime-type should be derived, not static.
        db.setex(hash + '_mime','image/jpeg',1000)
        return(hash)
    except:
        return("Failed to submit to server")

def sha256sum(data):
    d = sha256()
    d.update(data)
    return d.hexdigest()

@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    filedata = request.files['file'].read()
    print(request)
    print(filedata)
    print(sha256sum(filedata))
    # Check if the file is one of the allowed types/extensions
    if file:
        # Make the filename safe, remove unsupported chars
        filename = sha256sum(filedata)
        # Move the file form the temporal folder to
        # the upload folder we setup
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        redis_set(filename,filedata)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        # FIXME: I don't have any idea how to do this.
        return redirect("http://127.0.0.1:5000/files/" + str(filename))
#        return redirect(url_for('uploaded_file',
#                                filename=filename))

@app.route("/files/<hash>")
def redis_get(hash):
    upload_data = dbconn.get(hash)
    if upload_data is None:
        abort(404)
    mimetype = dbconn.get(hash + '_mime')
    response = make_response(upload_data)
    response.headers['Content-Type'] = mimetype
    #response.headers['Content-Disposition'] = 'attachment; filename=img.jpg'
    return(response)
    #return render_template("files.html",
    #    uuid=hash,
    #    files=image,
    #)


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))

app.run(debug=True)
