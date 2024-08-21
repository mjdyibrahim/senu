from flask import Blueprint, render_template, request

result_bp = Blueprint('result', __name__)

@result_bp.route('/result')
def show_result():
    scorecard = request.args.get('scorecard', '')
    return render_template('result.html', scorecard=scorecard)
