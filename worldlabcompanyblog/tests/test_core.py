import os,sys
import unittest

sys.path.append(os.path.abspath(os.path.join('..', '..')))
from worldlabcompanyblog import app, db
 
TEST_DB = 'test.db'
 
##test_basic.py is deleted update in gitbash and github



class BasicTests(unittest.TestCase):
 
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
 
    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Worldlab Company Blog', response.data)


    def test_home_page_blog_posts_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Title', response.data)
        self.assertIn(b'Hello Text', response.data)
        self.assertIn(b'Worldlab Company Blog', response.data)
        self.assertNotIn(b'Update', response.data)

    def test_home_page_blog_posts_without_logging_in(self):  #test is positive
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Title', response.data)
        self.assertIn(b'Hello Text', response.data)
        self.assertIn(b'Worldlab Company Blog', response.data)
        self.assertIn(b'Log In', response.data)


    def test_about_us_page(self):
        response = self.app.get('/info', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Info about our Company', response.data)

 
if __name__ == "__main__":
    unittest.main()