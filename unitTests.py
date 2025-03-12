import unittest
from app import app

class FlaskAppFunctionalTests(unittest.TestCase):

    def setUp(self):
        # Set up the Flask application for testing
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_register_page(self):
        # Test if the register page loads successfully
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)  # Check for a keyword in the HTML

    def test_register_user(self):
        # Test user registration
        registerResponse = self.client.post('/register', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        response = self.client.get('/login')
        self.assertEqual(registerResponse.status_code, 302)  # Expect a redirect after successful registration
        self.assertIn(b'Registration successful!', response.data)  # Check for success message

    def test_register_existing_user(self):
        # Test registration with an already existing email

        response = self.client.post('/register', data={
            'email': 'testuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)  # Expect to stay on the same page
        self.assertIn(b'Email already registered.', response.data)  # Check for error message

    def test_login_page(self):
        # Test if the login page loads successfully
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Check for a keyword in the HTML

    def test_login_user(self):
        # Test user login
        loginResponse = self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        response = self.client.get('/')
        self.assertEqual(loginResponse.status_code, 302)  # Expect a redirect after successful login
        self.assertIn(b'Login successful!', response.data)  # Check for success message

    def test_login_invalid_user(self):
        # Test login with invalid credentials
        response = self.client.post('/login', data={
            'email': 'invaliduser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Expect to stay on the same page
        self.assertIn(b'Login failed. Check your email and/or password.', response.data)  # Check for error message

    def test_logout_user(self):
        # Test user logout
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })  # Log in the user

        logoutResponse = self.client.post('/logout')
        response = self.client.get('/')
        self.assertEqual(logoutResponse.status_code, 302)  # Expect a redirect after logout
        self.assertIn(b'You have been logged out.', response.data)  # Check for logout message

    def test_entries_page(self):
        # Test if the entries page loads successfully when logged in
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })  # Log in the user

        response = self.client.get('/entries')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Entry', response.data)  # Check for a keyword in the HTML
    def test_delete_user(self):
        # Test user logout
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })  # Log in the user

        response = self.client.post('/delete')
        self.assertEqual(response.status_code, 302)  # Expect a redirect after logout
        self.assertIn(b'You have been deleted.', response.data)  # Check for logout message

if __name__ == '__main__':
    unittest.main()