import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin



app = Flask(__name__)

#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################
secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key

#################################
### DATABASE SETUPS ############
###############################

app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///'+ os.path.join(app.config['BASEDIR'], 'data.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)
@app.before_first_request
def create_tables():
	db.create_all()

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"

###########################
#### Admin CONFIGS #######
#########################

from worldlabcompanyblog.models import MyAdminIndexView, User, MyModelView, LogoutMenuLink, BlogPost
admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view = MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(BlogPost, db.session))
# # admin.add_link(LoginMenuLink(name='Login', category='', url="admins.admin_login"))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/admin_logout"))

###########################
#### BLUEPRINT CONFIGS #######
#########################
from worldlabcompanyblog.core.views import core
from worldlabcompanyblog.users.views import users
from worldlabcompanyblog.blog_posts.views import blog_posts
from worldlabcompanyblog.error_pages.handlers import error_pages
from worldlabcompanyblog.admins.views import admins

# Register the apps
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(admins)
