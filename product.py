from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from supabase_client import insert_product, get_products

product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/')
def show_product():
    products = get_products()
    print("Products from DB:", products)  # debug ดูข้อมูลที่ได้
    return render_template('product.html', products=products)

@product_bp.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        product_data = {
            'product_id': request.form.get('product_id'),
            'sample_date': request.form.get('sample_date'),
            'owner': request.form.get('owner'),
            'product_spec': request.form.get('product_spec'),
            'lot': request.form.get('lot'),
            'document_date': request.form.get('document_date'),
            'item': request.form.get('item'),
            'lab_no': request.form.get('lab_no'),
            'project_code': request.form.get('project_code')
        }
        session['pending_product'] = product_data
        return redirect(url_for('product.confirm_item'))

    return render_template('add_item.html')

@product_bp.route('/confirm', methods=['GET', 'POST'])
def confirm_item():
    product = session.get('pending_product')
    if not product:
        return redirect(url_for('product.add_item'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'yes':
            products = get_products()
            if any(p['product_id'] == product['product_id'] for p in products):
                flash(f"❌ รหัสสินค้า '{product['product_id']}' ซ้ำกัน กรุณาใช้รหัสอื่น")
                return redirect(url_for('product.add_item'))

            insert_product(product)
            session.pop('pending_product', None)
            flash(f"✅ เพิ่มสินค้า '{product['product_id']}' เรียบร้อยแล้ว")
            return redirect(url_for('product.show_product'))
        else:
            return redirect(url_for('product.add_item'))

    return render_template('confirm_item.html', product=product)

@product_bp.route('/send', methods=['POST'])
def send_to_lab():
    selected_codes = request.form.getlist('selected_items')
    selected_lab = request.form.get('lab_choice')

    if not selected_codes or not selected_lab:
        flash("⚠️ กรุณาเลือกสินค้าและเลือกแล็บก่อนส่ง")
        return redirect(url_for('product.show_product'))

    session['sent_data'] = {
        'product_codes': selected_codes,
        'lab': selected_lab
    }

    if selected_lab == 'chem':
        return redirect(url_for('chem.chem_home'))
    elif selected_lab == 'microbio':
        return redirect(url_for('micro.micro_home'))
    elif selected_lab == 'physic':
        return redirect(url_for('physic.physic_home'))
    else:
        flash('แล็บที่เลือกไม่ถูกต้อง')
        return redirect(url_for('product.show_product'))
