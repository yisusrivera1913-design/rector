from flask import Flask
from forms import LoginForm
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

def test_form():
    with app.app_context():
        form = LoginForm()
        form.cedula.data = '123456789'
        print('Form valid:', form.validate())
        print('Errors:', form.errors)

if __name__ == "__main__":
    test_form()
