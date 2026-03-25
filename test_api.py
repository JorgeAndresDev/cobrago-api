import requests
import uuid

BASE_URL = "http://localhost:8000/api/v1"

def print_result(step, response):
    print(f"--- {step} ---")
    print(f"Status Code: {response.status_code}")
    try:
        print(response.json())
    except:
        print(response.text)
    print("")
    return response

def test_api():
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    password = "password123"

    # 1. Register
    resp = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "full_name": "Test User",
        "password": password
    })
    print_result("REGISTER USER", resp)

    # 2. Login
    resp = requests.post(f"{BASE_URL}/auth/login", data={
        "username": email,
        "password": password
    })
    token_data = print_result("LOGIN USER", resp).json()
    token = token_data.get("access_token")
    if not token:
        print("Login failed, aborting tests.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Client
    resp = requests.post(f"{BASE_URL}/clients/", headers=headers, json={
        "nombre": "Juan Perez",
        "cedula": f"V-{uuid.uuid4().hex[:8]}",
        "direccion": "Calle Falsa 123",
        "monto_total": 1000.0,
        "synced": False
    })
    client_data = print_result("CREATE CLIENT", resp).json()
    client_id = client_data.get("id")

    # 4. Get Client
    resp = requests.get(f"{BASE_URL}/clients/{client_id}", headers=headers)
    print_result("GET CLIENT", resp)

    # 5. Register Payment
    resp = requests.post(f"{BASE_URL}/payments/", headers=headers, json={
        "monto": 250.0,
        "client_id": client_id,
        "synced": False
    })
    print_result("CREATE PAYMENT 1", resp)
    
    resp = requests.post(f"{BASE_URL}/payments/", headers=headers, json={
        "monto": 100.0,
        "client_id": client_id,
        "synced": False
    })
    print_result("CREATE PAYMENT 2", resp)

    # 6. Check Saldo
    resp = requests.get(f"{BASE_URL}/clients/{client_id}/saldo", headers=headers)
    print_result("GET CLIENT SALDO", resp)

    # 7. Check Abonos
    resp = requests.get(f"{BASE_URL}/clients/{client_id}/abonos", headers=headers)
    print_result("GET CLIENT ABONOS", resp)
    
    # 8. List Clients
    resp = requests.get(f"{BASE_URL}/clients/", headers=headers)
    print_result("LIST ALL CLIENTS", resp)

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"Error running tests: {e}")
