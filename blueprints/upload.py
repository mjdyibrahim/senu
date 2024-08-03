from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import dsp

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_pitch_deck():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads/pitch_decks', filename))
            pitch_deck_text = dsp.process_pitch_deck(filename)
            scorecard, scores = dsp.generate_scorecard(pitch_deck_text)
            dsp.generate_spider_graph(scores)
            return redirect(url_for('result.show_result', scorecard=scorecard))
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'ppt', 'pptx'}
