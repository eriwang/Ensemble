import os

from flask import Blueprint, abort, jsonify, request, send_file
from pydub import AudioSegment
from werkzeug.utils import secure_filename

import api.api_utils as au

_MERGED_TRACKS_FOLDER = os.path.join(os.getcwd(), 'merged_tracks')
_UPLOADED_TRACKS_FOLDER = os.path.join(os.getcwd(), 'uploaded_tracks')

track_bp = Blueprint('track', __name__)


@track_bp.route('/track', methods=['POST'])
@au.api_jsonify_errors
def upload_track():
    if 'file' not in request.files:
        raise au.BadRequestException('Expected "file" parameter in form data')

    file = request.files['file']
    filename = file.filename

    if filename == '':
        raise au.BadRequestException('No selected file')

    if not _is_file_allowed(filename):
        raise au.BadRequestException(f'Disallowed extension for filename {filename}')

    full_filepath = os.path.join(_UPLOADED_TRACKS_FOLDER, secure_filename(filename))
    if os.path.exists(full_filepath):
        raise au.BadRequestException(f'Filename {filename} already exists')

    if not os.path.exists(_UPLOADED_TRACKS_FOLDER):
        os.makedirs(_UPLOADED_TRACKS_FOLDER)

    file.save(full_filepath)
    return jsonify(success=True), 200


# TODO: caching
@track_bp.route('/merge', methods=['POST'])
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

    filename = 'merge.mp3'
    full_filepath = os.path.join(_MERGED_TRACKS_FOLDER, filename)
    # TODO: different types/ settings
    audio_segment.export(full_filepath, format='mp3')

    return jsonify({'filename': filename}), 200


# TODO: rethink what exactly this looks like with file previews and whatnot. Static instead?
@track_bp.route('/download', methods=['GET'])
@au.api_jsonify_errors
def download_track():
    _PARAM_KEY_TO_REQUIRED_VALUE_TYPES = {
        'is_merged': 'boolstr',
        'filename': str
    }

    params = au.validate_and_load_params(request.args, _PARAM_KEY_TO_REQUIRED_VALUE_TYPES)

    file_directory = _MERGED_TRACKS_FOLDER if params['is_merged'] else _UPLOADED_TRACKS_FOLDER
    full_filename = os.path.join(file_directory, params['filename'])
    if not os.path.exists(full_filename):
        abort(404)

    return send_file(full_filename, as_attachment=True)


def _is_file_allowed(filename):
    _, ext = os.path.splitext(filename)
    return ext in ('.wav', '.mp3')
