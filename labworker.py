from flask import Blueprint, render_template
from supabase_client import get_employees

labworker_bp = Blueprint('labworker', __name__, url_prefix='/labworker')

labworkers = get_employees()

@labworker_bp.route('/')
def labworker_home():
    print("Employees from DB:", labworkers)
    return render_template('labworker.html', workers=labworkers)

@labworker_bp.route('/<name>')
def show_labworker(name):
    for worker in labworkers:
        print(name)      
        print(worker.get("name",name))
        print(worker)  
        if worker.get("name",name) == name:
            return render_template('labworker_detail.html', worker=worker)
            
    return "ไม่พบเจ้าหน้าที่คนนี้", 404    
