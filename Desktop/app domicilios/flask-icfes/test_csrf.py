from app import create_app
app = create_app()
with app.test_client() as client:
    resp = client.get('/admin/login')
    print('GET /admin/login status:', resp.status_code)
    data = resp.get_data(as_text=True)
    print('Response data contains csrf_token:', 'csrf_token' in data)
    print('Response data contains form:', '<form' in data)
