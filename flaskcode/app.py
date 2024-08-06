from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/entrepreneur')
def entrepreneur_dashboard():
    return render_template('entrepreneur.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Handle authentication here
        return redirect(url_for('entrepreneur_dashboard'))
    return render_template('signin.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pitch_deck' in request.files:
        pitch_deck = request.files['pitch_deck']
        # Handle file upload
        return redirect(url_for('entrepreneur_dashboard'))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
