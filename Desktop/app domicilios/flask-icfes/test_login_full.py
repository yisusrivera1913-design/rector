from flask import Flask
from auth import auth_bp
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(auth_bp)

def test_login():
    with app.test_client() as client:
        # Test login with cedula that has access
        resp = client.post('/login', data={'cedula': '123456789'}, follow_redirects=True)
        print('Status:', resp.status_code)
        print('Location:', resp.headers.get('Location'))
        print('Data preview:', resp.get_data(as_text=True)[:500])

if __name__ == "__main__":
    test_login()
