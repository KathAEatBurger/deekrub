from flask import Blueprint, render_template, request, url_for

product_bp = Blueprint('product', __name__, url_prefix='/product')

# ตัวอย่าง mapping product_code -> labworker name
product_labworker_map = {
    'P001': 'Alice',
    'P002': 'Bob',
    'P003': 'Charlie',
}

@product_bp.route('/')
def show_product():
    product_code = request.args.get('product_code', 'ไม่พบข้อมูล')
    labworker_name = product_labworker_map.get(product_code)

    # สร้าง URL สำหรับลิงก์ไปหน้า labworker รายบุคคล
    labworker_url = None
    if labworker_name:
        labworker_url = url_for('labworker.show_labworker', name=labworker_name)

    return render_template('product.html', 
                           product_code=product_code,
                           labworker_name=labworker_name,
                           labworker_url=labworker_url)
