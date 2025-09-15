from flask import Blueprint, render_template, request

product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/')
def show_product():
    product_code = request.args.get('product_code', 'ไม่พบข้อมูล')
    return render_template('product.html', product_code=product_code)
