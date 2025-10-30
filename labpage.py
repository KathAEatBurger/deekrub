# labpage.py
from flask import Blueprint, render_template
from labmicro import micro_bp
from labchem import chem_bp
from labphysic import physic_bp

lab_bp = Blueprint('lab', __name__, url_prefix='/lab')

@lab_bp.route('/')
def lab_home():
    return render_template('lab.html')

# ==================== Register 3 lab blueprints ====================
# Microbiology
lab_bp.register_blueprint(micro_bp, url_prefix='/micro')
# Chemistry
lab_bp.register_blueprint(chem_bp, url_prefix='/chem')
# Physics
lab_bp.register_blueprint(physic_bp, url_prefix='/physic')
