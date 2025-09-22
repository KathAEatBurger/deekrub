from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

micro_bp = Blueprint('micro', __name__, url_prefix='/lab/micro')

UPLOAD_FOLDER = 'uploads/micro'  # โฟลเดอร์เก็บไฟล์
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'}  # นามสกุลที่อนุญาต

# ตรวจสอบว่านามสกุลไฟล์อนุญาตหรือไม่
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@micro_bp.route('/', methods=['GET', 'POST'])
def micro_home():
    products = ['Micro Product 1', 'Micro Product 2', 'Micro Product 3']

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
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # สร้างโฟลเดอร์หากยังไม่มี
            file.save(save_path)
            flash(f'อัปโหลดไฟล์เรียบร้อย: {filename}')
            return redirect(url_for('micro.micro_home'))

        else:
            flash('ประเภทไฟล์ไม่รองรับ')
            return redirect(request.url)

    return render_template('micro.html', products=products)
