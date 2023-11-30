import getpass
import unittest

from flask.cli import FlaskGroup

from src import app, db
from src.food.models import User

cli = FlaskGroup(app)

@cli.command('list_routes')
def list_routes():
    for url in app.url_map.iter_rules():
        print("%s %s %s" % (url.rule, url.methods, url.endpoint))



@cli.command("create_admin")
def create_admin():
    """Creates the admin user."""
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    phone = input("Enter phone number: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(fname=fname, lname=lname, phone=phone, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        print(f"Admin with name {fname + ' ' + lname} created successfully!")
    except Exception:
        print("Couldn't create admin user.")

if __name__ == "__main__":
    cli()

