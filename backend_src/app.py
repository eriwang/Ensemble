import os

from flask import Flask, render_template

from api.track_api import track_bp

_MERGED_TRACKS_FOLDER = os.path.join(os.getcwd(), 'merged_tracks')
_UPLOADED_TRACKS_FOLDER = os.path.join(os.getcwd(), 'uploaded_tracks')

app = Flask(__name__, static_folder='static_gen')
app.register_blueprint(track_bp)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
