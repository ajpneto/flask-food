from decouple import config
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config.from_object(config("APP_SETTINGS"))

configure_uploads = configure_uploads(app, photos)
#app.app_context()

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
migrate = Migrate(app, db)


from .auth.models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(user_id)


# Registering modules
from .auth import create_module as auth_create_module
auth_create_module(app)

from .admin import create_module as admin_create_module
admin_create_module(app)

from .food import create_module as food_create_module
food_create_module(app)

