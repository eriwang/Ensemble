import os

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static_gen')


@app.route('/track_upload', methods=['POST'])
def upload_track():
    if 'file' not in request.files:  # TODO: is this the input name?
        return jsonify({'error': 'No file in request files'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    _, ext = os.path.splitext(file.filename)
    if file and ext == '.wav':
        filename = secure_filename(file.filename)
        file.save(filename)
        return jsonify(success=True), 200

    return jsonify({'error': f'Disallowed filename {file.filename}'}), 400


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
