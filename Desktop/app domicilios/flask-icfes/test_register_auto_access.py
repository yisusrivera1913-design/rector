from app import create_app
app = create_app()
with app.test_client() as client:
    # Test registration
    get_resp = client.get('/register')
    data = get_resp.get_data(as_text=True)
    import re
    csrf_match = re.search(r'id="csrf_token" name="csrf_token" type="hidden" value="([^"]*)"', data)
    csrf_token = csrf_match.group(1) if csrf_match else None
    print('CSRF token found for register:', csrf_token[:10] + '...' if csrf_token else 'None')

    if csrf_token:
        # Register a new user
        resp = client.post('/register', data={
            'csrf_token': csrf_token,
            'nombre': 'Test Auto User',
            'cedula': '999999999'
        }, follow_redirects=True)
        print('Registration status:', resp.status_code)
        print('Registration response contains success:', 'Registrado con éxito' in resp.get_data(as_text=True))

        # Now test admin panel auto-grant
        # First login as admin
        get_admin_resp = client.get('/admin/login')
        admin_data = get_admin_resp.get_data(as_text=True)
        admin_csrf_match = re.search(r'id="csrf_token" name="csrf_token" type="hidden" value="([^"]*)"', admin_data)
        admin_csrf_token = admin_csrf_match.group(1) if admin_csrf_match else None
        print('Admin CSRF token found:', admin_csrf_token[:10] + '...' if admin_csrf_token else 'None')

        if admin_csrf_token:
            admin_resp = client.post('/admin/login', data={
                'csrf_token': admin_csrf_token,
                'password': 'admin123'
            }, follow_redirects=True)
            print('Admin login status:', admin_resp.status_code)
            print('Admin panel contains auto-grant message:', 'acceso automático' in admin_resp.get_data(as_text=True))
            print('Admin panel contains users:', 'Test Auto User' in admin_resp.get_data(as_text=True))
