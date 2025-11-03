from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from supabase_client import SUPABASE_URL, headers
import requests

login_bp = Blueprint("login", __name__)

@login_bp.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        url = f"{SUPABASE_URL}/rest/v1/employee?username=eq.{username}&select=*"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if not data:
                flash("❌ ไม่พบผู้ใช้ในระบบ", "danger")
            else:
                employee = data[0]
                if employee["password"] == password:
                    session["user"] = employee["username"]
                    session["role"] = employee.get("role", "user")
                    session["name"] = employee.get("name", employee["username"])  # <-- เพิ่มตรงนี้
                    flash("✅ เข้าสู่ระบบสำเร็จ", "success")
                    return redirect(url_for("home"))
                else:
                    flash("❌ รหัสผ่านไม่ถูกต้อง", "danger")
        else:
            flash("เกิดข้อผิดพลาดในการเชื่อมต่อกับฐานข้อมูล", "warning")

    return render_template("login.html")


@login_bp.route("/logout")
def logout():
    session.clear()
    flash("ออกจากระบบเรียบร้อยแล้ว", "info")
    return redirect(url_for("login.login"))
