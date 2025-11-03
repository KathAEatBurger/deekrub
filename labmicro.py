# labmicro.py
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from supabase_client import get_products, insert_sample_prep,update_product_preped_status
from functools import wraps
import datetime
import uuid

micro_bp = Blueprint("micro", __name__, url_prefix="/lab/micro")

# ตรวจสอบ login ก่อนเข้าใช้งาน
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("⚠️ กรุณาเข้าสู่ระบบก่อนใช้งาน", "warning")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated

@micro_bp.route("/", methods=["GET", "POST"])
@login_required
def micro_home():
    products = [p for p in get_products() if p.get("lab_type") == "microbio"]

    if request.method == "POST":
        prep_id = str(uuid.uuid4())
        prepared_by = session.get("user")
        date = datetime.date.today().isoformat()
        selected_products = request.form.getlist("selected_products")

        if not prep_id or not prepared_by or not date:
            flash("⚠️ กรุณากรอก Prep ID, Prepared By และ Date", "warning")
            return redirect(url_for("lab.micro.micro_home"))

        if not selected_products:
            flash("⚠️ กรุณาเลือกสินค้าอย่างน้อย 1 รายการ", "warning")
            return redirect(url_for("lab.micro.micro_home"))

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
                update_product_preped_status(product_id)
            else:
                flash(f"❌ ไม่สามารถบันทึกสินค้า {product_id}: {response}", "danger")

        flash(f"✅ บันทึกสินค้าสำหรับ prep_id '{prep_id}' จำนวน {success_count} รายการเรียบร้อยแล้ว")
        return redirect(url_for("lab.micro.micro_home"))

    return render_template("micro.html", products=products)
