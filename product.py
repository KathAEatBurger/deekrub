from flask import Blueprint, render_template, request, redirect, url_for, session, flash

product_bp = Blueprint('product', __name__, url_prefix='/product')

# จำลองฐานข้อมูลสินค้าในรูปแบบ list
products = []

@product_bp.route('/')
def show_product():
    return render_template('product.html', products=products)

@product_bp.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        product_data = {
            'code': request.form.get('product_code'),
            'sender': request.form.get('sender_name'),
            'type': request.form.get('product_type'),
            'lab_number': request.form.get('lab_number')
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
            # เช็ครหัสสินค้าซ้ำ
            if any(p['code'] == product['code'] for p in products):
                flash(f"❌ รหัสสินค้า '{product['code']}' ซ้ำกัน กรุณาใช้รหัสอื่น")
                return redirect(url_for('product.add_item'))

            products.append(product)
            session.pop('pending_product', None)
            flash(f"✅ เพิ่มสินค้า '{product['code']}' เรียบร้อยแล้ว")
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
