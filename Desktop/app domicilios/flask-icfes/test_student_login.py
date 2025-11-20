from app import create_app
app = create_app()
with app.test_client() as client:
    # First get the login form to get CSRF token
    get_resp = client.get('/login')
    data = get_resp.get_data(as_text=True)
    print('Login form contains form tag:', '<form' in data)
    print('Login form contains cedula input:', 'name="cedula"' in data)
    # Extract CSRF token
    import re
    csrf_match = re.search(r'id="csrf_token" name="csrf_token" type="hidden" value="([^"]*)"', data)
    csrf_token = csrf_match.group(1) if csrf_match else None
    print('CSRF token found:', csrf_token[:10] + '...' if csrf_token else 'None')

    if csrf_token:
        # Test login with cedula that has access
        resp = client.post('/login', data={'cedula': '123456789', 'csrf_token': csrf_token}, follow_redirects=True)
        print('POST /login status:', resp.status_code)
        print('Response location:', resp.headers.get('Location'))
        print('Response data contains success:', 'Inicio de sesión exitoso' in resp.get_data(as_text=True))
        print('Response data contains no access:', 'Aún no tienes acceso' in resp.get_data(as_text=True))
        print('Response data contains student panel:', 'Panel de' in resp.get_data(as_text=True))
        if 'Panel de' in resp.get_data(as_text=True):
            print('SUCCESS: Student login worked!')
        else:
            print('FAILED: Student login did not work')
            print('Response data preview:', resp.get_data(as_text=True)[:500])
    else:
        print('No CSRF token found in form')
