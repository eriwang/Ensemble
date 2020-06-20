import os

from flask import Flask, jsonify, render_template, request, send_file
from pydub import AudioSegment
from werkzeug.utils import secure_filename

_MERGED_TRACKS_FOLDER = os.path.join(os.getcwd(), 'merged_tracks')
_UPLOADED_TRACKS_FOLDER = os.path.join(os.getcwd(), 'uploaded_tracks')
app = Flask(__name__, static_folder='static_gen')


# TODO: jsonify 400 should be an exception that gets handled somehow
@app.route('/track', methods=['POST'])
def upload_track():
    if 'file' not in request.files:
        return jsonify({'error': 'No file in request files'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not _is_file_allowed(file.filename):
        return jsonify({'error': f'Disallowed extension for filename {file.filename}'}), 400

    full_filepath = os.path.join(_UPLOADED_TRACKS_FOLDER, secure_filename(file.filename))
    if os.path.exists(full_filepath):
        return jsonify({'error': 'Filename already exists'}), 400

    if not os.path.exists(_UPLOADED_TRACKS_FOLDER):
        os.makedirs(_UPLOADED_TRACKS_FOLDER)

    file.save(full_filepath)
    return jsonify(success=True), 200


# TODO: caching
@app.route('/merge', methods=['POST'])
def merge_tracks():
    audio_segments = []
    for f in os.listdir(_UPLOADED_TRACKS_FOLDER):
        if not _is_file_allowed(f):
            raise ValueError(f'Found unsupported file {f} in {_UPLOADED_TRACKS_FOLDER}')
        audio_segments.append(AudioSegment.from_file(os.path.join(_UPLOADED_TRACKS_FOLDER, f)))

    if len(audio_segments) == 0:
        raise ValueError(f'Cannot merge, no files found in {_UPLOADED_TRACKS_FOLDER}')

    # TODO: doesn't do any checking of length, maybe should take the longest
    audio_segment = audio_segments.pop()
    for a in audio_segments:
        audio_segment = audio_segment.overlay(a)

    if not os.path.exists(_MERGED_TRACKS_FOLDER):
        os.makedirs(_MERGED_TRACKS_FOLDER)

    full_filepath = os.path.join(_MERGED_TRACKS_FOLDER, 'merge.mp3')
    # TODO: different types/ settings
    audio_segment.export(full_filepath, format='mp3')

    return send_file(full_filepath, as_attachment=True)
    # return jsonify(success=True), 200


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


def _is_file_allowed(filename):
    _, ext = os.path.splitext(filename)
    return ext in ('.wav', '.mp3')


if __name__ == '__main__':
    app.run(debug=True)
