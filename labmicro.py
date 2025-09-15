from flask import Blueprint, render_template

micro_bp = Blueprint('micro', __name__, url_prefix='/lab/micro')

@micro_bp.route('/')
def micro_home():
    products = ['Micro Product 1', 'Micro Product 2', 'Micro Product 3']
    return render_template('micro.html', products=products)
