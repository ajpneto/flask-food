import functools
from flask import flash, redirect, url_for, session, abort
from flask_login import current_user
from flask_login import LoginManager, login_user
from flask_bcrypt import Bcrypt
from flask_login import AnonymousUserMixin

class AppAnonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = 'Guest'

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"
login_manager.anonymous_user = AppAnonymous


def create_module(app, **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .views import auth_bp
    app.register_blueprint(auth_bp)

def authenticate(phone, password):
    from .models import User
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return None
    # Do the passwords match
    if not user.check_password(password):
        return None
    return user


def identity(payload):
    return load_user(payload['identity'])


def has_role(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.has_role(name):
                return f(*args, **kwargs)
            else:
                abort(403)

        return functools.update_wrapper(wraps, f)

    return real_decorator


@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)


