from . import bcrypt, AnonymousUserMixin
from .. import db

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer, index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20), nullable=False, index=True, unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
#    posts = db.relationship('Post', backref='user', lazy='dynamic')

    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )


    def __init__(self, name, age, address, phone, email, password, is_admin=False):
        default = Role.query.filter_by(name="default").one()
        self.roles.append(default)
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'is_admin':self.is_admin
        }


    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
        return False


    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)
