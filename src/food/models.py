from datetime import datetime
from .. import db

class MenuItem(db.Model):

    item_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255), default='')
    desc = db.Column(db.String(255))
    pic = db.Column(db.String(100))
    price = db.Column(db.String(5), default='0')

    def __str__(self):
        return self.name

class Rating(db.Model):
    r_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    r_date = db.Column(db.DateTime(), default=datetime.now())

    def __str__(self):
        return f"{self.name}\'s review"


class Order(db.Model):
    order_id = db.Column(db.Integer(), primary_key=True)
    items_json = db.Column(db.String(5000))
    name = db.Column(db.String(255), default='')
    phone = db.Column(db.String(255), default='')
    table = db.Column(db.String(255), default='take away')
    price = db.Column(db.String(255), default='0')
    order_time = db.Column(db.DateTime(), default=datetime.now())
    bill_clear = db.Column(db.Boolean(), default=False)


class Bill(db.Model):
    bill_id = db.Column(db.Integer(), primary_key=True)
    order_items = db.Column(db.String(5000))
    name = db.Column(db.String(50), default='')
    bill_total = db.Column(db.Integer())
    phone = db.Column(db.String(25))
    bill_time = db.Column(db.DateTime(), default=datetime.now())


class BookTable(db.Model):
    book_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), default='')
    phone = db.Column(db.String(25))
    bdate = db.Column(db.String(50))
    btime = db.Column(db.String(50))
    num_peoples = db.Column(db.Integer(), default=1)
    special = db.Column(db.String(255))
