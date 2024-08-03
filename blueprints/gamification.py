from flask import Blueprint, render_template
import dsp

gamification_bp = Blueprint('gamification', __name__)

@gamification_bp.route('/gamification')
def show_gamification():
    challenges = dsp.get_gamified_challenges()
    return render_template('gamification.html', challenges=challenges)
