# supabase_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")

# Headers สำหรับ Supabase REST API
headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"  # ให้ response แสดง row ที่สร้าง/อัปเดต
}

# ==================== Products ====================
def insert_product(data):
    """เพิ่มสินค้าใหม่"""
    url = f"{SUPABASE_URL}/rest/v1/lab_product"
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"error": "Invalid JSON response"}

    print("Insert response:", response.status_code, response_data)
    print("Response:", response.text)  # <--- ดูว่ามี error จาก Supabase หรือไม่
    return response_data, response.status_code

def get_products():
    """ดึงรายการสินค้า"""
    url = f"{SUPABASE_URL}/rest/v1/lab_product?select=*"
    response = requests.get(url, headers=headers)
    try:
        products = response.json()
        # แปลง sent เป็น Boolean จริง
        for p in products:
            if 'sent' in p:
                p['sent'] = str(p['sent']).lower() == 'true'

        # DEBUG: แสดงค่า lab_type ของทุก product
        for p in products:
            print(f"DEBUG: product_id={p.get('product_id')}, lab_type={p.get('lab_type')}, sent={p.get('sent')}")

        return products
    except ValueError:
        return []

def update_product_lab_info(product_id, lab_no, lab_type, org_code):
    """อัปเดตข้อมูล lab ของสินค้า"""
    data = {
        "sent": True,
        "lab_no": lab_no,
        "lab_type": lab_type,
        "org_code": org_code
    }
    url = f"{SUPABASE_URL}/rest/v1/lab_product?product_id=eq.{product_id}"
    
    # DEBUG: ดู URL และ payload
    print("DEBUG: PATCH URL:", url)
    print("DEBUG: PATCH DATA:", data)
    
    response = requests.patch(url, json=data, headers=headers)
    
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"error": "Invalid JSON response"}
    
    # DEBUG: ดูผลลัพธ์จาก Supabase
    print(f"Update {product_id} response:", response.status_code, response_data)
    print("Response text:", response.text)
    
    return response_data, response.status_code

def update_product_sent_status(product_id, lab):
    """อัปเดตสถานะสินค้าเป็นส่งแล้ว พร้อมระบุแล็บ"""
    data = {"preped": True, "lab_no": lab}
    url = f"{SUPABASE_URL}/rest/v1/lab_product?product_id=eq.{product_id}"
    response = requests.patch(url, json=data, headers=headers)
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"error": "Invalid JSON response"}

    print("Update sent_status response:", response.status_code, response_data)
    return response_data, response.status_code

# ==================== Sample Prep ====================
import json

def insert_sample_prep(data):
    """
    เพิ่มข้อมูลลง sample_prep table
    data = {
        "prep_id": str,       # ต้องระบุ
        "prepared_by": str,   # ต้องระบุ
        "product_id": str,    # อาจมีหรือไม่ก็ได้
        "lab_no": str,        # อาจมีหรือไม่ก็ได้
        "date": str           # ต้องกรอกเป็น YYYY-MM-DD
    }
    """
    url = f"{SUPABASE_URL}/rest/v1/sample_prep"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"error": "Invalid JSON response"}

    print("Insert sample_prep response:", response.status_code, response_data)
    return response_data, response.status_code


def update_product_preped_status(product_id):
    data = {"preped": True}
    url = f"{SUPABASE_URL}/rest/v1/lab_product?product_id=eq.{product_id}"
    response = requests.patch(url, json=data, headers=headers)
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"error": "Invalid JSON response"}

    print("Update sent_status response:", response.status_code, response_data)
    return response_data, response.status_code
# ==================== Employees ====================
def get_employees():
    url = f"{SUPABASE_URL}/rest/v1/employee?select=*"
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except ValueError:
        return []

# ==================== Lab ====================
def get_lab():
    url = f"{SUPABASE_URL}/rest/v1/lab?select=*"
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except ValueError:
        return []

def get_micro_samples():
    """ดึงข้อมูลสินค้าจาก table lab_sample"""
    url = f"{SUPABASE_URL}/rest/v1/lab_sample?select=*"
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except ValueError:
        return []
    
def get_sample_preps():
    """
    ดึงข้อมูลทั้งหมดจากตาราง sample_prep ผ่าน REST API
    คืนค่าเป็น list ของ dict
    """
    url = f"{SUPABASE_URL}/rest/v1/sample_prep?select=*"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            preps = response.json()
            # แปลงค่าที่ควรเป็น boolean เช่น sent ถ้ามี
            for p in preps:
                if 'sent' in p:
                    p['sent'] = str(p['sent']).lower() == 'true'
            return preps
        else:
            print(f"❌ Supabase error {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Exception in get_sample_preps(): {e}")
        return []
    
def insert_report(data):
    """
    เพิ่มข้อมูล report
    data = {
        "report_id": str,       # ต้องระบุ
        "prep_id": str,         # อ้างอิงจาก sample_prep
        "test_date": str,       # YYYY-MM-DD
        "tested_by": str,       # ผู้ทดสอบ
        "result_data": str,     # ข้อมูลผลการทดลอง
        "username": str,        # username ของคนบันทึก
        "status": str           # เช่น 'pending'
    }
    """
    url = f"{SUPABASE_URL}/rest/v1/report"
    response = requests.post(url, headers=headers, json=data)
    try:
        return response.json(), response.status_code
    except ValueError:
        return {"error": "Invalid JSON response"}, response.status_code

# ==================== Debug ====================
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {'SET' if SUPABASE_API_KEY else 'NOT SET'}")

def debug_get_products():
    """Debug function: ดึง products พร้อมแสดงรายละเอียด request/response"""
    if not SUPABASE_URL or not SUPABASE_API_KEY:
        print("❌ SUPABASE_URL หรือ SUPABASE_KEY ไม่ถูกตั้งค่า")
        return []

    url = f"{SUPABASE_URL}/rest/v1/lab_product?select=*"
    print("DEBUG: GET URL:", url)
    print("DEBUG: HEADERS:", headers)

    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print("❌ Exception during request:", e)
        return []

    print("DEBUG: STATUS CODE:", response.status_code)
    print("DEBUG: RESPONSE TEXT:", response.text)

    try:
        products = response.json()
        print("DEBUG: RESPONSE JSON:", products)
        # แปลง sent เป็น Boolean จริง
        for p in products:
            if 'sent' in p:
                p['sent'] = str(p['sent']).lower() == 'true'

        # DEBUG: แสดงค่า lab_type ของทุก product
        for p in products:
            print(f"DEBUG: product_id={p.get('product_id')}, lab_type={p.get('lab_type')}, sent={p.get('sent')}")
    except ValueError:
        print("❌ Response is not valid JSON")
        products = []

    return products

if __name__ == "__main__":
    print("=== TESTING get_products() ===")
    products = get_products()
    print("Products:", products)
