from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from supabase_client import get_sample_preps, insert_report
from functools import wraps
import datetime
import uuid

scientist_bp = Blueprint("scientist", __name__, url_prefix="/scientist")

# ----------------------------
# Decorators
# ----------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("⚠️ กรุณาเข้าสู่ระบบก่อนใช้งาน", "warning")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated

def scientist_or_lead_required(f):
    """
    อนุญาตเฉพาะผู้ใช้ที่มี role เป็น Scientist หรือ Team Lead
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("⚠️ กรุณาเข้าสู่ระบบก่อนใช้งาน", "warning")
            return redirect(url_for("login.login"))
        
        role = session.get("role", "").lower()
        if role not in ["scientist", "team lead"]:
            flash("❌ คุณไม่มีสิทธิ์เข้าถึงหน้านี้ (เฉพาะ Scientist หรือ Team Lead เท่านั้น)", "danger")
            return redirect(url_for("home"))
        
        return f(*args, **kwargs)
    return decorated

# ----------------------------
# Routes
# ----------------------------

@scientist_bp.route("/", methods=["GET", "POST"])
@scientist_or_lead_required
def scientist_home():
    sample_preps = get_sample_preps()

    if request.method == "POST":
        selected_preps = request.form.getlist("selected_prep")
        username = session.get("user")
        today = datetime.date.today().isoformat()

        for prep_id in selected_preps:
            result_data = request.form.get(f"result_{prep_id}", "").strip()
            if not result_data:
                continue  # ข้ามถ้าไม่ได้กรอกผลการทดลอง

            report_data = {
                "report_id": str(uuid.uuid4()),
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
