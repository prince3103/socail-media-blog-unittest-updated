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

    def update_blog_post(self, post_id, title, text):
        return self.app.post(
            post_id+'/update',
            data= dict(title=title, text=text), 
            follow_redirects=True)


###############
#### tests ####
###############

########----22 may to be recorded in excel sheet

    def test_404_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        response = self.app.get('/2', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 Page Not Found!', response.data)


    def test_403_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.register('prince@gmail.com', 'prince1', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        self.app.get('/logout', follow_redirects=True)
        self.login('prince@gmail.com', 'FlaskIsAwesome')
        response = self.update_blog_post('1', 'New Title', 'New Text')
        self.assertEqual(response.status_code, 403)
        self.assertIn(b'403 Access Forbidden!', response.data)


if __name__ == "__main__":
    unittest.main()