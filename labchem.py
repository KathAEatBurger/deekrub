from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from supabase_client import get_products, insert_sample_prep  # ใช้ฟังก์ชันเดียวกับ physic/micro
from functools import wraps

chem_bp = Blueprint("chem", __name__, url_prefix="/chem")

# ตรวจสอบ login
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("⚠️ กรุณาเข้าสู่ระบบก่อนใช้งาน", "warning")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated

@chem_bp.route("/", methods=["GET", "POST"])
@login_required
def chem_home():
    products = [p for p in get_products() if p.get("lab_type") == "chem"]

    if request.method == "POST":
        prep_id = request.form.get("prep_id")
        prepared_by = request.form.get("prepared_by")
        date = request.form.get("date")
        selected_products = request.form.getlist("selected_products")

        if not prep_id or not prepared_by or not date:
            flash("⚠️ กรุณากรอก Prep ID, Prepared By และ Date", "warning")
            return redirect(url_for("chem.chem_home"))

        if not selected_products:
            flash("⚠️ กรุณาเลือกสินค้าอย่างน้อย 1 รายการ", "warning")
            return redirect(url_for("chem.chem_home"))

        success_count = 0
        for product_id in selected_products:
            lab_no = next((p["lab_no"] for p in products if p["product_id"] == product_id), None)
            response, status = insert_sample_prep({
                "prep_id": prep_id,
                "date": date,
                "product_id": product_id,
                "lab_no": lab_no,
                "prepared_by": prepared_by
            })
            if status in (200, 201):
                success_count += 1
            else:
                flash(f"❌ ไม่สามารถบันทึกสินค้า {product_id}: {response}", "danger")

        flash(f"✅ บันทึกสินค้าสำหรับ prep_id '{prep_id}' จำนวน {success_count} รายการเรียบร้อยแล้ว")
        return redirect(url_for("chem.chem_home"))

    return render_template("chem.html", products=products)
