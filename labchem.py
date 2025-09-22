from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

chem_bp = Blueprint('chem', __name__, url_prefix='/lab/chem')

UPLOAD_FOLDER = 'uploads/chem'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@chem_bp.route('/', methods=['GET', 'POST'])
def chem_home():
    products = ['Chemical Product 1', 'Chemical Product 2']

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
            return redirect(url_for('chem.chem_home'))
        else:
            flash('ประเภทไฟล์ไม่รองรับ')
            return redirect(request.url)

    return render_template('chem.html', products=products)
