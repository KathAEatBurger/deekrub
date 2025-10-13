import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "lab_product"  # เปลี่ยนตามชื่อ table

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def insert_product(data):
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    response = requests.post(url, json=data, headers=headers)
    print("Insert response:", response.status_code, response.json())  # debug ดูผลตอบกลับจาก supabase
    return response.json(), response.status_code

def get_products():
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?select=*"
    response = requests.get(url, headers=headers)
    return response.json()

print(f"URL: {SUPABASE_URL}")
print(f"API Key: {SUPABASE_API_KEY}")