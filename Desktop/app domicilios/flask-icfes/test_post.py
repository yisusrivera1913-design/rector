from app import create_app
app = create_app()
with app.test_client() as client:
    # First get the form to get CSRF token
    get_resp = client.get('/admin/login')
    data = get_resp.get_data(as_text=True)
    print('Form HTML contains hidden csrf_token input:', 'type="hidden" name="csrf_token"' in data)
    print('Form HTML contains form tag:', '<form' in data)
    print('Form HTML contains password input:', 'name="password"' in data)
    # Extract CSRF token from the form
    import re
    csrf_match = re.search(r'id="csrf_token" name="csrf_token" type="hidden" value="([^"]*)"', data)
    csrf_token = csrf_match.group(1) if csrf_match else None
    print('CSRF token found:', csrf_token[:10] + '...' if csrf_token else 'None')
    print('Full HTML snippet around form:')
    start = data.find('<form')
    end = data.find('</form>') + 7
    print(data[start:end])

    if csrf_token:
        resp = client.post('/admin/login', data={'password': 'admin123', 'csrf_token': csrf_token})
        print('POST /admin/login status:', resp.status_code)
        print('Response location:', resp.headers.get('Location'))
        print('Response data contains error:', 'Clave admin incorrecta' in resp.get_data(as_text=True))
        print('Response data contains success redirect:', 'admin_panel' in str(resp.headers.get('Location')))
        if resp.status_code == 302:
            print('SUCCESS: Admin login worked!')
        else:
            print('FAILED: Admin login did not work')
    else:
        print('No CSRF token found in form')
