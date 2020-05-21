import os,sys
import unittest

sys.path.append(os.path.abspath(os.path.join('..', '..')))
from worldlabcompanyblog import app, db
from worldlabcompanyblog.models import User
 
TEST_DB = 'admin.db'
 	

 
class AdminsTests(unittest.TestCase):
 
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


	def admin_login(self, email, password):
	    return self.app.post(
	        '/admin_login',
	        data=dict(email=email, password=password),
	        follow_redirects=True
	    )



	###############
	#### tests ####
	###############

	def test_admin_login_form_displays(self):
	    response = self.app.get('/admin_login')
	    self.assertEqual(response.status_code, 200)
	    self.assertIn(b'Admin Log In', response.data)


	def test_valid_admin_login(self):
	    self.app.get('/register', follow_redirects=True)
	    self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
	    self.app.get('/admin_login', follow_redirects=True)
	    response = self.admin_login('patkennedy79@gmail.com', 'FlaskIsAwesome')
	    self.assertIn(b'Logout', response.data)


	def test_admin_login_without_registering(self):
	    self.app.get('/admin_login', follow_redirects=True)
	    response = self.admin_login('patkennedy79@gmail.com', 'FlaskIsAwesome')
	    self.assertIn(b'Invalid Email Address or Password', response.data)


	def test_missing_email_field_admin_login_error(self):
	    self.app.get('/admin_login', follow_redirects=True)
	    response = self.admin_login('', 'FlaskIsAwesome')
	    self.assertIn(b'This field is required.', response.data)


	def test_missing_password_field_user_login_error(self):
	    self.app.get('/admin_login', follow_redirects=True)
	    response = self.admin_login('patkennedy79@gmail.com', '')
	    self.assertIn(b'This field is required.', response.data)


	def test_admin_form_displays(self):
		self.app.get('/register', follow_redirects=True)
		self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
		self.app.get('/admin_login', follow_redirects=True)
		response = self.admin_login('patkennedy79@gmail.com', 'FlaskIsAwesome')
		self.assertIn(b'Logout', response.data)
		response = self.app.get('/admin', follow_redirects=True)
		self.assertIn(b'Admin', response.data)
		self.assertIn(b'Home', response.data)
		self.assertIn(b'User', response.data)
		self.assertIn(b'Blog Post', response.data)


	def test_admin_site_user_valid_access(self):
		self.app.get('/register', follow_redirects=True)
		response = self.register('prince@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Thanks for registering! Now you can login!', response.data)
		self.app.get('/admin_login', follow_redirects=True)
		response = self.admin_login('prince@gmail.com', 'FlaskIsAwesome')
		self.assertIn(b'Admin', response.data)
		self.assertIn(b'Logged in successfully.', response.data)
		response = self.app.get('/admin/user/')
		self.assertIn(b'Profile Image', response.data)
		self.assertIn(b'Email', response.data)
		self.assertIn(b'Username', response.data)
		self.assertIn(b'Password Hash', response.data)


	def test_admin_site_user_invalid_access(self):
		response = self.app.get('/admin/user/')
		self.assertEqual(response.status_code, 302)
		self.assertIn(b'You should be redirected automatically to target URL:', response.data)
		self.assertIn(b'<a href="/admin_login">/admin_login</a>', response.data)


	def test_admin_site_blogpost_valid_access(self):
		self.app.get('/register', follow_redirects=True)
		response = self.register('prince@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Thanks for registering! Now you can login!', response.data)
		self.app.get('/admin_login', follow_redirects=True)
		response = self.admin_login('prince@gmail.com', 'FlaskIsAwesome')
		self.assertIn(b'Admin', response.data)
		self.assertIn(b'Logged in successfully.', response.data)
		response = self.app.get('admin/blogpost/')
		self.assertIn(b'Users', response.data)
		self.assertIn(b'Date', response.data)
		self.assertIn(b'Title', response.data)
		self.assertIn(b'Text', response.data)
		self.assertIn(b'Author', response.data)

	def test_admin_site_blogpost_invalid_access(self):
		response = self.app.get('/admin/blogpost/')
		self.assertEqual(response.status_code, 302)
		self.assertIn(b'You should be redirected automatically to target URL:', response.data)
		self.assertIn(b'<a href="/admin_login">/admin_login</a>', response.data)



	def test_valid_logout(self):
	    self.app.get('/register', follow_redirects=True)
	    self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
	    self.app.get('/admin_login', follow_redirects=True)
	    self.admin_login('patkennedy79@gmail.com', 'FlaskIsAwesome')
	    response = self.app.get('/admin_logout', follow_redirects=True)
	    self.assertIn(b'You are logged out!', response.data)


	def test_invalid_logout_within_being_logged_in(self):
	    response = self.app.get('/admin_logout', follow_redirects=True)
	    self.assertIn(b'Register', response.data)
	    self.assertIn(b'Log In', response.data)


if __name__ == "__main__":
    unittest.main()

