import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def insert_product(data):
    url = f"{SUPABASE_URL}/rest/v1/lab_product"
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"error": "Invalid JSON response"}

    print("Insert response:", response.status_code, response_data)
    return response_data, response.status_code

def get_employees():
    url = f"{SUPABASE_URL}/rest/v1/employee?select=*"
    response = requests.get(url, headers=headers)
    return response.json()

def get_products():
    url = f"{SUPABASE_URL}/rest/v1/lab_product?select=*"
    response = requests.get(url, headers=headers)
    return response.json()
    
def get_lab():
    url = f"{SUPABASE_URL}/rest/v1/lab?select=*"
    response = requests.get(url, headers=headers)
    return response.json()

print(f"URL: {SUPABASE_URL}")
print(f"API Key: {SUPABASE_API_KEY}")

if __name__ == "__main__":
    print("=== TESTING get_products() ===")
    products = get_products()
    print("Response from Supabase:", products)
