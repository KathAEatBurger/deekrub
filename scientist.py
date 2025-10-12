from flask import Blueprint, request, render_template, session, redirect, url_for

scientist_bp = Blueprint('scientist', __name__, url_prefix='/lab/scientist')

# เก็บข้อมูลสินค้าที่ได้รับจากแต่ละ lab ใน session
# ตัวอย่างเก็บข้อมูลแบบ session['scientist_data'] = {'chem': [...], 'micro': [...], 'physic': [...]}

@scientist_bp.route('/', methods=['GET', 'POST'])
def scientist_home():
    if 'scientist_data' not in session:
        session['scientist_data'] = {'chem': [], 'micro': [], 'physic': []}

    if request.method == 'POST':
        # สมมติ lab จะส่งมาใน form hidden input ชื่อ lab_name
        lab_name = request.form.get('lab_name')
        selected_items = request.form.getlist('selected_items')

        # อัพเดตข้อมูลใน session
        data = session['scientist_data']
        if lab_name in data:
            # อัพเดตรายการสินค้าใน lab นั้น (replace หรือ append ตามต้องการ)
            data[lab_name] = selected_items
            session['scientist_data'] = data

        return redirect(url_for('scientist.scientist_home'))

    # ดึงข้อมูลจาก session มาแสดง
    scientist_data = session.get('scientist_data', {})

    return render_template('sci.html', scientist_data=scientist_data)
