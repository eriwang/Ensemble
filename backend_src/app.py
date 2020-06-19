import os

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

_UPLOADED_TRACKS_FOLDER = './uploaded_tracks'
app = Flask(__name__, static_folder='static_gen')


# TODO: jsonify 400 should be an exception that gets handled somehow
@app.route('/track', methods=['POST'])
def upload_track():
    if 'file' not in request.files:
        return jsonify({'error': 'No file in request files'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    _, ext = os.path.splitext(file.filename)
    if ext != '.wav':
        return jsonify({'error': f'Disallowed extension for filename {file.filename}'}), 400

    full_filepath = os.path.join(_UPLOADED_TRACKS_FOLDER, secure_filename(file.filename))
    if os.path.exists(full_filepath):
        return jsonify({'error': f'Filename already exists'}), 400

    if not os.path.exists(_UPLOADED_TRACKS_FOLDER):
        os.makedirs(_UPLOADED_TRACKS_FOLDER)

    file.save(full_filepath)
    return jsonify(success=True), 200


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
