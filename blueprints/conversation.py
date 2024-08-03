from flask import Blueprint, render_template, request, redirect, url_for
import extractsections

conversation_bp = Blueprint('conversation', __name__)

@conversation_bp.route('/conversation', methods=['GET', 'POST'])
def conversation():
    if request.method == 'POST':
        user_data = {
            "Company Name": request.form['company_name'],
            "Date Started": request.form['date_started'],
            "Registered": request.form['registered'],
            "User Contact Info": request.form['contact_info'],
            "Number of Co-Founders": int(request.form['cofounders']),
            "Cofounder Education": request.form['cofounder_education'],
            "Cofounder Startup Experience": request.form['cofounder_experience'],
            "Cofounder Successful Exit": request.form['cofounder_exit'],
            "Category of Tasks and Competence": request.form['team_competence']
        }
        scorecard, scores = extractsections.generate_scorecard(user_data)
        extractsections.generate_spider_graph(scores)
        return redirect(url_for('result.show_result'))
    return render_template('conversation.html')
