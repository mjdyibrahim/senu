from flask import Blueprint, render_template
import falcon

roadmap_bp = Blueprint('roadmap', __name__)

@roadmap_bp.route('/roadmap')
def show_milestones():
    milestones = falcon.generate_milestones()
    return render_template('roadmap.html', milestones=milestones)
