from app import create_app
import os
os.environ['ADMIN_PASSWORD'] = 'admin123'
app = create_app()
with app.test_client() as client:
    # Test GET /admin/login
    resp = client.get('/admin/login')
    print('GET /admin/login status:', resp.status_code)
    data = resp.get_data(as_text=True)
    print('Response contains csrf_token:', 'csrf_token' in data)
    print('Response contains form:', '<form' in data)

    # Extract CSRF token
    import re
    csrf_match = re.search(r'id="csrf_token" name="csrf_token" type="hidden" value="([^"]*)"', data)
    csrf_token = csrf_match.group(1) if csrf_match else None
    print('CSRF token extracted:', csrf_token[:10] + '...' if csrf_token else 'None')

    # Test POST with correct password
    if csrf_token:
        resp = client.post('/admin/login', data={'password': 'admin123', 'csrf_token': csrf_token})
        print('POST /admin/login status:', resp.status_code)
        print('Redirect location:', resp.headers.get('Location'))
        if resp.status_code == 302 and '/admin/panel' in str(resp.headers.get('Location')):
            print('SUCCESS: Admin login worked!')
        else:
            print('FAILED: Admin login did not work')

    # Test POST with wrong password
    resp = client.post('/admin/login', data={'password': 'wrongpassword', 'csrf_token': csrf_token})
    print('POST /admin/login (wrong password) status:', resp.status_code)
    data = resp.get_data(as_text=True)
    print('Response contains error message:', 'Clave admin incorrecta' in data)
    print('Response contains flashed messages:', 'error' in data or 'Clave admin incorrecta' in data)
    print('Full response data:', data[:500] + '...' if len(data) > 500 else data)
    print('Flashed messages in response:', 'error' in data)
