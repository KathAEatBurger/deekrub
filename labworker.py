from flask import Blueprint, render_template

# Create the blueprint
labworker_bp = Blueprint('labworker', __name__, url_prefix='/labworker')

# In-memory "database" of lab workers
labworkers = {
    'Alice': {
        'name': 'Alice',
        'role': 'Chemist',
        'email': 'alice@lab.com'
    },
    'Bob': {
        'name': 'Bob',
        'role': 'Technician',
        'email': 'bob@lab.com'
    },
    'Charlie': {
        'name': 'Charlie',
        'role': 'Analyst',
        'email': 'charlie@lab.com'
    }
}

# Home route: list all labworkers
@labworker_bp.route('/')
def labworker_home():
    return render_template('labworker.html', workers=labworkers.values())

# Detail route: show info for a specific labworker
@labworker_bp.route('/<name>')
def show_labworker(name):
    worker = labworkers.get(name)
    if not worker:
        return "ไม่พบเจ้าหน้าที่คนนี้", 404
    return render_template('labworker_detail.html', worker=worker)
