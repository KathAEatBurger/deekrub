from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
from product import get_products  # แก้ไข: import ฟังก์ชัน get_products แทน products

chem_bp = Blueprint('chem', __name__, url_prefix='/lab/chem')

UPLOAD_FOLDER = 'uploads/chem'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@chem_bp.route('/', methods=['GET', 'POST'])
def chem_home():
    # ดึงข้อมูลสินค้าทุกครั้งที่โหลดหน้า
    all_products = get_products()

    # ดึงข้อมูลสินค้าที่ส่งมาจาก session
    sent_data = session.pop('sent_data', None)  # pop เพื่อใช้ครั้งเดียว
    sent_products = []

    if sent_data and sent_data.get('lab') == 'chem':  # ตรวจสอบว่าเลือก lab chem
        selected_codes = sent_data.get('product_codes', [])
        # กรองสินค้าที่มี product_code ตรงกับที่เลือกส่งมา
        sent_products = [p for p in all_products if p.get('product_code') in selected_codes]

    # อัปโหลดไฟล์
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ไม่พบไฟล์ที่อัปโหลด')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('ยังไม่ได้เลือกไฟล์')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            try:
                file.save(save_path)
                flash(f'✅ อัปโหลดไฟล์เรียบร้อย: {filename}')
            except Exception as e:
                flash(f'❌ เกิดข้อผิดพลาดในการบันทึกไฟล์: {e}')
            return redirect(url_for('chem.chem_home'))
        else:
            flash('❌ ประเภทไฟล์ไม่รองรับ')
            return redirect(request.url)

    return render_template('chem.html', products=sent_products)
