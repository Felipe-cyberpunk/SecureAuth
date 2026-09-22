import requests

BASE_URL = "http://127.0.0.1:8000"

def test_security_controls():
    print("[*] Iniciando auditoría de seguridad automatizada...")

    # 1. Prueba de acceso no autorizado a ruta protegida (simulando atacante sin token)
    print("\n[Prueba 1] Intentando acceder a ruta protegida sin token...")
    response = requests.get(f"{BASE_URL}/users/me") # O cambia por tu ruta protegida real
    if response.status_code == 401:
        print("[✔] ¡Éxito! El servidor bloqueó el acceso no autorizado (HTTP 401).")
    else:
        print(f"[✖] Alerta: El servidor respondió con un código inesperado: {response.status_code}")

    # 2. Prueba de autenticación con credenciales falsas
    print("\n[Prueba 2] Intentando iniciar sesión con credenciales inválidas...")
    payload = {
        "username": "hacker_falso",
        "password": "wrongpassword123"
    }
    response = requests.post(f"{BASE_URL}/token", data=payload)
    if response.status_code == 400 or response.status_code == 401:
        print("[✔] ¡Éxito! Las credenciales incorrectas fueron rechazadas correctamente.")
    else:
        print(f"[✖] Alerta: Comportamiento inusual en el login: {response.status_code}")

if __name__ == "__main__":
    test_security_controls()