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


    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )



    ###############
    #### tests ####
    ###############

    def test_create_post_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/create', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Title', response.data)
        self.assertIn(b'Text', response.data)


    def test_create_post(self):
        pass


    def test_create_post_missing_title_field(self):
        pass


    def test_create_post_missing_text_field(self):
        pass


    
 
if __name__ == "__main__":
    unittest.main()
