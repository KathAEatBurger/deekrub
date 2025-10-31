from flask import Blueprint, make_response, render_template, session, redirect, url_for, flash, request
import requests
import os
from datetime import date
from dotenv import load_dotenv
import pdfkit

# กำหนด path ของ wkhtmltopdf
config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

load_dotenv()

report_bp = Blueprint("report", __name__, url_prefix="/report")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

# ดึงข้อมูลทั้งหมด
def get_reports():
    url = f"{SUPABASE_URL}/rest/v1/report?select=*"
    response = requests.get(url, headers=headers)
    return response.json()

# ดึงข้อมูลรายงานเดียว
def get_report_by_id(report_id):
    url = f"{SUPABASE_URL}/rest/v1/report?report_id=eq.{report_id}&select=*"
    response = requests.get(url, headers=headers)
    data = response.json()
    if data:
        return data[0]
    return None

# อัปเดตสถานะเป็น approved
def approve_route(report_id):
    url = f"{SUPABASE_URL}/rest/v1/report?report_id=eq.{report_id}"
    data = {
        "status": "approved",
        "approval_date": str(date.today())
    }
    response = requests.patch(url, json=data, headers=headers)
    return response.status_code

# อัปเดตสถานะเป็น published
def publish_report(report_id):
    url = f"{SUPABASE_URL}/rest/v1/report?report_id=eq.{report_id}"
    data = {
        "status": "published"
    }
    response = requests.patch(url, json=data, headers=headers)
    return response.status_code

# หน้าแสดงรายงานหลัก (pending / approved)
@report_bp.route("/")
def report_home():
    if "user" not in session:
        return redirect(url_for("login.login"))

    reports = get_reports()
    pending_reports = [r for r in reports if r.get("status") == "pending"]
    approved_reports = [r for r in reports if r.get("status") == "approved"]

    return render_template(
        "report.html",
        username=session["user"],
        pending_reports=pending_reports,
        approved_reports=approved_reports
    )

# ดูรายละเอียดและแก้ไขรายงาน
@report_bp.route("/view/<report_id>", methods=["GET", "POST"])
def view_report(report_id):
    if "user" not in session:
        return redirect(url_for("login.login"))

    if request.method == "POST":
        old_id = request.form["old_report_id"]
        new_id = request.form["report_id"]

        data = {
            "report_id": new_id,
            "test_date": request.form["test_date"],
            "tested_by": request.form["tested_by"],
            "result_data": request.form.get("result_data"),
            "remarks": request.form.get("remarks")
        }

        url = f"{SUPABASE_URL}/rest/v1/report?report_id=eq.{old_id}"
        response = requests.patch(url, json=data, headers=headers)

        if response.status_code in (200, 204):
            flash(f"✅ แก้ไขรายงาน {old_id} เป็น {new_id} เรียบร้อยแล้ว", "success")
        else:
            flash("❌ เกิดข้อผิดพลาดในการแก้ไขรายงาน", "error")

        return redirect(url_for("report.view_report", report_id=new_id))

    report = get_report_by_id(report_id)
    if not report:
        flash("❌ ไม่พบรายงานนี้", "error")
        return redirect(url_for("report.report_home"))

    return render_template("report_detail.html", username=session["user"], report=report)

# อนุมัติรายงาน
@report_bp.route("/approve/<report_id>", methods=["POST"])
def approve_report(report_id):
    url = f"{SUPABASE_URL}/rest/v1/report?report_id=eq.{report_id}"
    data = {
        "status": "approved",
        "approval_date": str(date.today())
    }
    response = requests.patch(url, json=data, headers=headers)
    
    if response.status_code in (200, 204):
        flash(f"✅ รายงาน {report_id} อนุมัติเรียบร้อยแล้ว", "success")
    else:
        flash("❌ เกิดข้อผิดพลาดในการอนุมัติ", "error")
    
    return redirect(url_for("report.report_home"))

# เผยแพร่รายงาน
@report_bp.route("/publish/<report_id>", methods=["POST"])
def publish_route(report_id):
    if "user" not in session:
        return redirect(url_for("login.login"))

    status_code = publish_report(report_id)
    if status_code in (200, 204):
        flash(f"🚀 เผยแพร่รายงาน {report_id} เรียบร้อยแล้ว", "success")
    else:
        flash("❌ เกิดข้อผิดพลาดในการเผยแพร่รายงาน", "error")

    return redirect(url_for("report.published_reports"))

# หน้า Published Reports
@report_bp.route("/published")
def published_reports():
    if "user" not in session:
        return redirect(url_for("login.login"))

    reports = get_reports()
    published = [r for r in reports if r.get("status") == "published"]

    return render_template(
        "published_reports.html",
        username=session["user"],
        published_reports=published
    )

# อัปโหลดลายเซ็นก่อนเผยแพร่รายงาน
@report_bp.route("/upload_signature/<report_id>", methods=["GET", "POST"])
def upload_signature(report_id):
    if "user" not in session:
        return redirect(url_for("login.login"))

    report = get_report_by_id(report_id)
    if not report:
        flash("❌ ไม่พบรายงานนี้", "error")
        return redirect(url_for("report.report_home"))

    if request.method == "POST":
        file = request.files.get("signature")
        if not file:
            flash("⚠️ กรุณาเลือกไฟล์ลายเซ็น", "error")
            return redirect(request.url)

        allowed_ext = {".png", ".jpg", ".jpeg"}
        _, ext = os.path.splitext(file.filename.lower())
        if ext not in allowed_ext:
            flash("❌ อนุญาตเฉพาะไฟล์ PNG หรือ JPG เท่านั้น", "error")
            return redirect(request.url)

        upload_folder = os.path.join("static", "signatures")
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"{report_id}{ext}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # อัปเดตสถานะเป็น published
        status_code = publish_report(report_id)
        if status_code in (200, 204):
            flash(f"✅ ลายเซ็นถูกอัปโหลดและรายงาน {report_id} เผยแพร่เรียบร้อยแล้ว", "success")
            # redirect ไปหน้า PDF แทน
            return redirect(url_for("report.view_report_pdf", report_id=report_id))
        else:
            flash("❌ เกิดข้อผิดพลาดในการเผยแพร่รายงาน", "error")

    return render_template("upload_signature.html", report=report)

@report_bp.route("/report/<report_id>/view_pdf")
def view_report_pdf(report_id):
    report = get_report_by_id(report_id)
    if not report:
        flash("❌ ไม่พบรายงาน", "error")
        return redirect(url_for("report.report_home"))

    # ตรวจสอบไฟล์เซ็น
    sig_folder = os.path.join("static", "signatures")
    sig_png = os.path.join(sig_folder, f"{report_id}.png")
    sig_jpg = os.path.join(sig_folder, f"{report_id}.jpg")

    if os.path.exists(sig_png):
        signature_file = f"signatures/{report_id}.png"
    elif os.path.exists(sig_jpg):
        signature_file = f"signatures/{report_id}.jpg"
    else:
        signature_file = None  # ไม่มีลายเซ็น

    return render_template(
        "report_pdf.html",
        report=report,
        signature_file=signature_file
    )

@report_bp.route("/report/<report_id>/pdf")
def report_pdf(report_id):
    report = get_report_by_id(report_id)
    if not report:
        flash("❌ ไม่พบรายงานนี้", "error")
        return redirect(url_for("report.report_home"))

    sig_folder = os.path.join("static", "signatures")
    sig_png = os.path.join(sig_folder, f"{report_id}.png")
    sig_jpg = os.path.join(sig_folder, f"{report_id}.jpg")

    if os.path.exists(sig_png):
        signature_file = sig_png  # ใช้ absolute path
    elif os.path.exists(sig_jpg):
        signature_file = sig_jpg
    else:
        signature_file = None

    if signature_file:
        # wkhtmltopdf ต้องใช้ file:///
        signature_file = f"file:///{os.path.abspath(signature_file).replace(os.sep, '/')}"


    # สร้าง HTML
    rendered = render_template("report_pdf_only.html", report=report, signature_file=signature_file)


    options = {
        'enable-local-file-access': None,
        'quiet': ''
    }

    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=report_{report_id}.pdf'
    return response
