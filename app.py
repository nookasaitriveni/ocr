from demo import fetch_ocr
import flask
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return "Use POST Method to upload files"
    if request.method == 'POST':
        files = flask.request.files.getlist("files")
        data = {}
        for file in files:
            file.save(secure_filename(file.filename))
            data[file.filename] = fetch_ocr(secure_filename(file.filename))
        return {
            "data": data
        }


if __name__ == '__main__':
    app.run(debug=True)
