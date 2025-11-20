from app import create_app
app = create_app()
with app.app_context():
    with app.test_request_context():
        from forms import AdminLoginForm
        form = AdminLoginForm()
        print('Form fields:', [f.name for f in form])
        print('CSRF token field:', hasattr(form, 'csrf_token'))
        print('Meta csrf:', form.meta.csrf)
        print('CSRF field name:', form.meta.csrf_field_name)
