# product.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from supabase_client import insert_product, get_products, update_product_lab_info
from functools import wraps
import uuid

product_bp = Blueprint('product', __name__, url_prefix='/product')

# ------------------ Decorators ------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("⚠️ กรุณาเข้าสู่ระบบก่อนใช้งาน", "warning")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated

def role_required(allowed_roles):
    """ตรวจสอบสิทธิ์การเข้าถึงหน้าตาม role"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            role = session.get("role", "").strip()
            # เปรียบเทียบแบบไม่สนตัวพิมพ์เล็ก/ใหญ่
            if role.lower() not in [r.lower() for r in allowed_roles]:
                flash("❌ คุณไม่มีสิทธิ์เข้าถึงหน้านี้", "danger")
                return redirect(url_for("home"))
            return f(*args, **kwargs)
        return decorated
    return decorator

# ------------------ Helper ------------------

def empty_to_none(val):
    return val if val and val.strip() else None

# ------------------ Routes ------------------

# ✅ แสดงรายการสินค้า
@product_bp.route('/')
@login_required
@role_required(["QA", "Lab", "Team Lead"])
def show_product():
    products = get_products()
    return render_template('product.html', products=products)

# ✅ เพิ่มสินค้าใหม่
@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required(["QA", "Lab", "Team Lead"])
def add_item():
    if request.method == 'POST':
        product_data = {
            'product_id': request.form.get('product_id'),
            'sample_date': request.form.get('sample_date'),
            'owner': session["user"],
            'product_spec': empty_to_none(request.form.get('product_spec')),
            'lot': empty_to_none(request.form.get('lot')),
            'document_date': empty_to_none(request.form.get('document_date')),
            'item': empty_to_none(request.form.get('item')),
            'lab_no': empty_to_none(request.form.get('lab_no')),
            'project_code': str(uuid.uuid4()),
            'sent': False
        }

        if not product_data['sample_date']:
            flash("⚠️ กรุณาระบุวันที่เก็บตัวอย่าง")
            return redirect(url_for('product.add_item'))

        session['pending_product'] = product_data
        return redirect(url_for('product.confirm_item'))

    return render_template('add_item.html')

# ✅ หน้ายืนยันก่อนบันทึกสินค้า
@product_bp.route('/confirm', methods=['GET', 'POST'])
@login_required
@role_required(["QA", "Lab", "Team Lead"])
def confirm_item():
    product = session.get('pending_product')
    if not product:
        flash("⚠️ ไม่มีสินค้าที่รอการยืนยัน")
        return redirect(url_for("product.show_product"))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'yes':
            products = get_products()
            if any(p['product_id'] == product['product_id'] for p in products):
                flash(f"❌ รหัสสินค้า '{product['product_id']}' ซ้ำ กรุณาใช้รหัสอื่น")
                return redirect(url_for('product.add_item'))

            response, status = insert_product(product)
            if status in [200, 201]:
                session.pop('pending_product', None)
                flash(f"✅ เพิ่มสินค้า '{product['product_id']}' เรียบร้อยแล้ว")
            else:
                flash(f"❌ เกิดข้อผิดพลาดในการบันทึกสินค้า: {response}")
            return redirect(url_for('product.show_product'))
        else:
            session.pop('pending_product', None)
            return redirect(url_for("product.show_product"))

    return render_template('confirm_item.html', product=product)

# ✅ ส่งสินค้าไปแลป
@product_bp.route('/send', methods=['POST'])
@login_required
@role_required(["Lab", "Team Lead"])
def send_to_lab():
    selected_codes = request.form.getlist('selected_items')
    if request.form.get('lab_choice') == "chem":
        selected_lab_no = "L02"
    elif request.form.get('lab_choice') == "microbio":
        selected_lab_no = "L01"
    elif request.form.get('lab_choice') == "physic":
        selected_lab_no = "L03"
    selected_lab_no = request.form.get('lab_choice')
    selected_lab_type = request.form.get('lab_choice')
    selected_lab_org = str(uuid.uuid4())

    if not selected_codes or not selected_lab_no or not selected_lab_type or not selected_lab_org:
        flash("⚠️ กรุณาเลือกสินค้าและกรอกข้อมูลแลปครบถ้วนก่อนส่ง")
        return redirect(url_for('product.show_product'))

    success_count = 0
    for code in selected_codes:
        response, status = update_product_lab_info(code, selected_lab_no, selected_lab_type, selected_lab_org)
        if status in (200, 201):
            success_count += 1
        else:
            flash(f"❌ ไม่สามารถอัปเดตสินค้า {code} ได้: {response.get('error')}", "danger")

    flash(f"✅ ส่งสินค้า {success_count} รายการไปแล็บ '{selected_lab_type}' เรียบร้อยแล้ว")
    return redirect(url_for('product.show_product'))
