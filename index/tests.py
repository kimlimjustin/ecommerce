from django.test import TestCase, Client
from .models import User, Items
# Create your tests here.

class TestPage(TestCase):
    def setUp(self):
        pass

    def test_response(self):
        c = Client()
        home = c.get('/')
        self.assertEqual(home.status_code, 200)
        create = c.get('/create')
        self.assertEqual(create.status_code, 302)
        login = c.get('/login')
        self.assertEqual(login.status_code, 200)
        register = c.get('/register')
        self.assertEqual(register.status_code, 200)
        cart = c.get('/cart')
        self.assertEqual(cart.status_code, 302)
        setting = c.get('/setting')
        self.assertEqual(setting.status_code, 302)
        dashboard = c.get('/dashboard')
        self.assertEqual(dashboard.status_code, 302)