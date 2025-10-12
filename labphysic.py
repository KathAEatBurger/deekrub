from flask import Blueprint, render_template, session
from product import products as all_products

physic_bp = Blueprint('physic', __name__, url_prefix='/lab/physic')

@physic_bp.route('/')
def physic_home():
    product_list = []
    sent_data = session.get('sent_data')
    if sent_data and sent_data.get('lab') == 'physic':
        codes = sent_data.get('product_codes', [])
        # ดึงสินค้าแบบเต็ม (dict) ที่มี code ตรงกับรหัสที่ส่งมา
        product_list = [p for p in all_products if p['code'] in codes]

    return render_template('physic.html', products=product_list)
