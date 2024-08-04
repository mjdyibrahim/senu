from flask import Blueprint, render_template
import extractsections

roadmap_bp = Blueprint('roadmap', __name__)

@roadmap_bp.route('/roadmap')
def show_milestones():
    milestones = extractsections.generate_milestones()
    return render_template('roadmap.html', milestones=milestones)
