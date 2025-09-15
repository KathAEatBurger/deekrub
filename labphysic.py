from flask import Blueprint, render_template

physic_bp = Blueprint('physic', __name__, url_prefix='/lab/physic')

@physic_bp.route('/')
def physic_home():
    products = ['Physics Product 1']
    return render_template('physic.html', products=products)
