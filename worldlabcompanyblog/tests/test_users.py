import os,sys
import unittest

sys.path.append(os.path.abspath(os.path.join('..', '..')))
from worldlabcompanyblog import app, db
from worldlabcompanyblog.models import User
from werkzeug.datastructures import FileStorage
 
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


    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )



    def create_post(self, title, text):
        return self.app.post(
            '/create',
            data = dict(title=title, text = text),
            follow_redirects=True)



    ###############
    #### tests ####
    ###############

#test for registration

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


    def test_logout_user_on_opening_registration_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/register', follow_redirects=True)
        self.assertIn(b'Log In', response.data)
        self.assertIn(b'Register', response.data)
        self.assertNotIn(b'Logout', response.data)


#test for login

    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create an Account', response.data)
        self.assertIn(b'Log In', response.data)


    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'Log Out', response.data)


    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'Invalid Email Address or Password', response.data)


    def test_missing_email_field_user_login_error(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('', 'FlaskIsAwesome')
        self.assertIn(b'This field is required.', response.data)


    def test_missing_password_field_user_login_error(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', '')
        self.assertIn(b'This field is required.', response.data)


    def test_logout_user_on_opening_login_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/login', follow_redirects=True)
        self.assertIn(b'Log In', response.data)
        self.assertNotIn(b'Logout', response.data)


#logout

    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'You are Logged Out', response.data)


    def test_invalid_logout_within_being_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Register', response.data)
        self.assertIn(b'Log In', response.data)


#user_accout_page

    def test_user_account_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/account')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the page for prince', response.data)
        self.assertIn(b'patkennedy79@gmail.com', response.data)


    def test_user_account_without_logging_in(self):
        response = self.app.get('/account')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Faccount', response.data)



    def test_update_profile_pic_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'samplepic', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/account')
        self.assertIn(b'src="/static/profile_pics/default_profile.jpg"', response.data)
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        current_file_dir = os.path.dirname(current_file_path)
        samplepic_path = os.path.join(current_file_dir, "static/profile_pics/one.png")

        my_file = FileStorage(
            stream=open(samplepic_path, "rb"),
            filename="samplepic.png",
            content_type="image/png",
        )
        response = self.app.post(
           '/account',
           data={
              "picture": my_file,
           },
           content_type="multipart/form-data"
        )

        response = self.app.get('/account')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'src="/static/profile_pics/samplepic.png"', response.data)


    def test_update_profile_pic_wihout_logging_in(self):
        response = self.app.get('/account')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Faccount', response.data)
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        current_file_dir = os.path.dirname(current_file_path)
        samplepic_path = os.path.join(current_file_dir, "static/profile_pics/one.png")

        my_file = FileStorage(
            stream=open(samplepic_path, "rb"),
            filename="samplepic.png",
            content_type="image/png",
        )
        response = self.app.post(
           '/account',
           data={
              "picture": my_file,
           },
           content_type="multipart/form-data"
        )

        response = self.app.get('/account')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Faccount', response.data)


    def test_user_blog_post_page_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/prince')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the page for prince', response.data)



    def test_user_blog_post_page_without_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/prince')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the page for prince', response.data)


    def test_user_blog_posts_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        response = self.app.get('/prince', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Title', response.data)
        self.assertIn(b'Hello Text', response.data)
        self.assertIn(b'Welcome to the page for prince', response.data)


    def test_user_blog_posts_without_logging_in(self): 
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/prince', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Title', response.data)
        self.assertIn(b'Hello Text', response.data)
        self.assertIn(b'Welcome to the page for prince', response.data)

 
if __name__ == "__main__":
    unittest.main()
