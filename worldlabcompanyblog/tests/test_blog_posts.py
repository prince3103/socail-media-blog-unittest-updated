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

    def delete_blog_post(self, post_id):
        return self.app.post(
            post_id+"/delete",
            follow_redirects=True)


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

#create new post

    def test_create_new_post_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        response = self.create_post('Hello Title', 'Hello Text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Worldlab Company Blog', response.data)
        self.assertIn(b'Hello Title', response.data)
        self.assertIn(b'Hello Text', response.data)

    def test_create_new_post_without_logging_in(self):
        self.app.get('/create', follow_redirects=True)
        response = self.create_post('Hello Title', 'Hello Text')
        self.assertIn(b'Log In', response.data)
        self.assertNotIn(b'Hello Title', response.data)

    def test_create_new_post_missing_title_field(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        response = self.create_post('', 'Hello Text')
        self.assertIn(b'This field is required.', response.data)

    def test_create_new_post_missing_text_field(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        response = self.create_post('Hello Title', '')
        self.assertIn(b'This field is required.', response.data)


#read blog posts
    def test_read_blog_post_with_valid_id_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        response = self.app.get('/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Title', response.data)
        self.assertIn(b'Hello Text', response.data)
        self.assertIn(b'Update', response.data)


    def test_read_blog_post_with_valid_id_without_logging_in(self):  #Positive
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Title', response.data)
        self.assertIn(b'Hello Text', response.data)
        self.assertNotIn(b'Update', response.data)
        self.assertIn(b'Register', response.data)


    def test_read_blog_post_with_invalid_id_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        response = self.app.get('/2', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 Page Not Found!', response.data)


#update blog post

    def test_update_post_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        response = self.app.get('/1/update', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Title', response.data)
        self.assertIn(b'Text', response.data)
        self.assertIn(b'Hello Title', response.data)
        self.assertIn(b'Hello Text', response.data)
        self.assertIn(b'Post', response.data)


    def test_update_blog_post_with_valid_author_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        response = self.update_blog_post('1', 'New Title', 'New Text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Title', response.data)
        self.assertIn(b'New Text', response.data)
        self.assertIn(b'Update', response.data)



    def test_update_blog_post_with_valid_author_without_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        self.app.get('/logout', follow_redirects=True)
        response = self.update_blog_post('1', 'New Title', 'New Text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertNotIn(b'New Text', response.data)
        self.assertNotIn(b'Update', response.data)



    def test_update_blog_post_with_invalid_author_after_logging_in(self):
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
        self.assertIn(b'Log Out', response.data)
        self.assertNotIn(b'New Title', response.data)


#delete blog post


    def test_delete_blog_post_with_valid_author_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        response = self.delete_blog_post('1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Worldlab Company Blog', response.data)
        self.assertNotIn(b'Hello Title', response.data)
        self.assertNotIn(b'Hello Text', response.data)



    def test_delete_blog_post_with_valid_author_without_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        self.app.get('/logout', follow_redirects=True)
        response = self.delete_blog_post('1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertNotIn(b'Hello Title', response.data)
        self.assertNotIn(b'Hello Text', response.data)



    def test_delete_blog_post_with_invalid_author_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'prince', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.register('prince@gmail.com', 'prince1', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.app.get('/create', follow_redirects=True)
        self.create_post('Hello Title', 'Hello Text')
        self.app.get('/logout', follow_redirects=True)
        self.login('prince@gmail.com', 'FlaskIsAwesome')
        response = self.delete_blog_post('1')
        self.assertEqual(response.status_code, 403)
        self.assertIn(b'403 Access Forbidden!', response.data)
        self.assertIn(b'Log Out', response.data)
        self.assertNotIn(b'New Title', response.data)


    

if __name__ == "__main__":
    unittest.main()
