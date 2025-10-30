from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from supabase_client import get_sample_preps, insert_report
from functools import wraps
import datetime
import uuid

scientist_bp = Blueprint("scientist", __name__, url_prefix="/scientist")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("⚠️ กรุณาเข้าสู่ระบบก่อนใช้งาน", "warning")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated

@scientist_bp.route("/", methods=["GET", "POST"])
@login_required
def scientist_home():
    sample_preps = get_sample_preps()

    if request.method == "POST":
        selected_preps = request.form.getlist("selected_prep")
        username = session.get("user")  # สมมติ session['user'] คือ username
        today = datetime.date.today().isoformat()

        for prep_id in selected_preps:
            result_data = request.form.get(f"result_{prep_id}", "").strip()
            if not result_data:
                continue  # ข้ามถ้าไม่กรอกผลการทดลอง

            report_data = {
                "report_id": str(uuid.uuid4()),  # สร้าง UUID เป็น PK
                "prep_id": prep_id,
                "test_date": today,
                "tested_by": username,
                "result_data": result_data,
                "username": username,
                "status": "pending"
            }
            resp, status = insert_report(report_data)
            print(f"Inserted report for {prep_id}: status={status}, resp={resp}")

        flash("✅ บันทึกผลการทดลองเรียบร้อยแล้ว", "success")
        return redirect(url_for("scientist.scientist_home"))

    return render_template("scientist.html", sample_preps=sample_preps)
