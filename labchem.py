from flask import Blueprint, render_template

chem_bp = Blueprint('chem', __name__, url_prefix='/lab/chem')

@chem_bp.route('/')
def chem_home():
    products = ['Chemical Product 1', 'Chemical Product 2']
    return render_template('chem.html', products=products)
