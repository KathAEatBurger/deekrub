from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from product import products as all_products

micro_bp = Blueprint('micro', __name__, url_prefix='/lab/micro')

"""UPLOAD_FOLDER = 'uploads/micro'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
"""
@micro_bp.route('/', methods=['GET', 'POST'])
def micro_home():
    # ดึงสินค้าที่ถูกส่งมาสำหรับแล็บ microbio
    product_list = []
    sent_data = session.get('sent_data')
    if sent_data and sent_data.get('lab') == 'microbio':
        codes = sent_data.get('product_codes', [])
        product_list = [p for p in all_products if p['code'] in codes]

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
                flash(f'อัปโหลดไฟล์เรียบร้อย: {filename}')
            except Exception as e:
                flash(f'เกิดข้อผิดพลาดในการบันทึกไฟล์: {e}')
            return redirect(url_for('micro.micro_home'))
        else:
            flash('ประเภทไฟล์ไม่รองรับ')
            return redirect(request.url)

    return render_template('micro.html', products=product_list)
