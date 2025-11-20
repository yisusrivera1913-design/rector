from app import create_app
app = create_app()
with app.test_client() as client:
    resp = client.get('/admin/login')
    data = resp.get_data(as_text=True)
    print('Full HTML response:')
    print(data)
