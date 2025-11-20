from flask import Flask
from auth import auth_bp
from config import DevelopmentConfig
from supabase_client import supabase
from encryption import hash_text
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(auth_bp)

# Test login logic
def test_login():
    with app.test_client() as client:
        # Test with cedula that has access
        cedula = '123456789'  # Test User
        cedula_hash = hash_text(cedula)
        print(f"Testing login with cedula: {cedula}, hash: {cedula_hash}")

        # Check DB
        resp = supabase.table("usuarios").select("*").eq("cedula_hash", cedula_hash).execute()
        print(f"DB query result: {resp.data}")

        if resp.data:
            user = resp.data[0]
            print(f"User found: {user['nombre']}, tiene_acceso: {user['tiene_acceso']}")

            if user.get("tiene_acceso", False):
                print("Should login successfully")
            else:
                print("Should deny access")
        else:
            print("User not found")

        # Test with cedula without access
        cedula2 = '987654321'  # Assume no access
        cedula_hash2 = hash_text(cedula2)
        print(f"\nTesting login with cedula: {cedula2}, hash: {cedula_hash2}")

        resp2 = supabase.table("usuarios").select("*").eq("cedula_hash", cedula_hash2).execute()
        print(f"DB query result: {resp2.data}")

if __name__ == "__main__":
    test_login()
