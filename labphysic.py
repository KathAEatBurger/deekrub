from flask import Blueprint, render_template, session
from product import get_products  # Import the function, not a variable

physic_bp = Blueprint('physic', __name__, url_prefix='/lab/physic')

@physic_bp.route('/')
def physic_home():
    product_list = []
    sent_data = session.get('sent_data')
    if sent_data and sent_data.get('lab') == 'physic':
        codes = sent_data.get('product_codes', [])
        # Fetch fresh products from DB
        all_products = get_products()
        # Filter products that match the sent codes
        product_list = [p for p in all_products if p.get('product_code') in codes]

    return render_template('physic.html', products=product_list)
