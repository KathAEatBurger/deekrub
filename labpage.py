from flask import Blueprint, render_template, request, redirect, url_for


lab_bp = Blueprint('lab', __name__, url_prefix='/lab')

@lab_bp.route('/')
def lab_home():
    return render_template('lab.html')


@lab_bp.route('/micro', methods=['GET', 'POST'])
def lab_micro():
    if request.method == 'POST':
        product_code = request.form['product_code']
        return redirect(url_for('product.show_product', product_code=product_code))
    return render_template('micro.html')

@lab_bp.route('/chem', methods=['GET', 'POST'])
def lab_chem():
    if request.method == 'POST':
        product_code = request.form['product_code']
        return redirect(url_for('product.show_product', product_code=product_code))
    return render_template('chem.html')

@lab_bp.route('/physic', methods=['GET', 'POST'])
def lab_physic():
    if request.method == 'POST':
        product_code = request.form['product_code']
        return redirect(url_for('product.show_product', product_code=product_code))
    return render_template('physic.html')
