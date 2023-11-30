from flask_admin import Admin
from .. import db
from .views import CustomModelView, CustomFileAdmin  #, PostView, CustomView
from src.auth.models import User, Role
from src.food.models import BookTable, Rating, MenuItem, Order, Bill
#from src.portfolio.models import Product
#from src.blog.models import Post, Comment, Tag

admin = Admin()


def create_module(app, **kwargs):
    admin.init_app(app)
#    admin.add_view(CustomView(name='AENTECH'))

    models = [User, Role, BookTable, Rating, MenuItem, Order, Bill]

    for model in models:
        admin.add_view(CustomModelView(model, db.session, category='Models'))

#    admin.add_view(PostView(Post, db.session, category='Models'))
    admin.add_view(CustomFileAdmin(app.static_folder, '/static/', name='Static Files'))
