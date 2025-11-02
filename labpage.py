# labpage.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps

from labmicro import micro_bp
from labchem import chem_bp
from labphysic import physic_bp

lab_bp = Blueprint('lab', __name__, url_prefix='/lab')

# ----------------------------
# Decorators
# ----------------------------

def login_required(f):
    """ตรวจสอบว่าเข้าสู่ระบบแล้ว"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("⚠️ กรุณาเข้าสู่ระบบก่อนใช้งาน", "warning")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated


def labworker_or_lead_required(f):
    """อนุญาตเฉพาะ Labworker หรือ Team Lead"""
    @wraps(f)
    def decorated(*args, **kwargs):
        role = session.get("role", "").strip().lower()
        if role not in ["labworker", "team lead"]:
            flash("❌ คุณไม่มีสิทธิ์เข้าถึงหน้านี้ (เฉพาะ Labworker หรือ Team Lead เท่านั้น)", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated

# ----------------------------
# Routes
# ----------------------------

@lab_bp.route('/')
@login_required
@labworker_or_lead_required
def lab_home():
    """หน้าเลือกประเภทแลป — เข้าได้เฉพาะ Labworker และ Team Lead"""
    return render_template('lab.html')

# ==================== Register 3 lab blueprints ====================
lab_bp.register_blueprint(micro_bp, url_prefix='/micro')
lab_bp.register_blueprint(chem_bp, url_prefix='/chem')
lab_bp.register_blueprint(physic_bp, url_prefix='/physic')
