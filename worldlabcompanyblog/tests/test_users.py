import os,sys
import unittest

sys.path.append(os.path.abspath(os.path.join('..', '..')))
from worldlabcompanyblog import app, db
from worldlabcompanyblog.models import User
 
TEST_DB = 'user.db'
 
 
class UsersTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        # Disable sending emails during unit testing
        # mail.init_app(app)
        # self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 



    ########################
    #### helper methods ####
    ########################

    def register(self, email, username, password, pass_confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, username=username, password=password, pass_confirm=pass_confirm),
            follow_redirects=True
        )


    ###############
    #### tests ####
    ###############

    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Already have an account?', response.data)


    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('prince@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thanks for registering! Now you can login!', response.data)


    def test_invalid_user_registration_different_passwords(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('prince@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsNotAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords Must Match!', response.data)


    def test_duplicate_email_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@yahoo.com', 'prince1', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.app.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@yahoo.com', 'prince', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
        self.assertIn(b'Your email has been registered already!', response.data)


    def test_duplicate_username_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('prince@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.app.get('/register', follow_redirects=True)
        response = self.register('prince1@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertIn(b'Sorry, that username is taken!', response.data)


    def test_missing_email_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('', 'prince', 'prince', 'prince')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)


    def test_missing_username_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('prince@gmail.com', '', 'prince', 'prince')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)


    def test_missing_password_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('prince@gmail.com', 'prince', '', 'prince')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)


    def test_missing_confirm_password_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('prince@gmail.com', 'prince', 'prince', '')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)


 
if __name__ == "__main__":
    unittest.main()
