from flask import Flask, render_template, request, redirect, url_for
from blueprints.upload import upload_bp
from blueprints.conversation import conversation_bp
from blueprints.result import result_bp
from blueprints.roadmap import roadmap_bp
from blueprints.gamification import gamification_bp

app = Flask(__name__)

app.register_blueprint(upload_bp)
app.register_blueprint(conversation_bp)
app.register_blueprint(result_bp)
app.register_blueprint(roadmap_bp)
app.register_blueprint(gamification_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
