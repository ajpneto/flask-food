from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required
from .. import db
from .models import User
from .forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__)

#@auth_bp.route('/')
#def index():
#    return render_template('server_table.html', title='Server-Driven Table')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login(page=1):
    if current_user.is_authenticated:
        flash("You are already logged in.", category="info")
        return redirect(url_for('food.home'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user:
            login_user(user)
            flash("You have been logged in.", category="success")
            return redirect(url_for("food.home"))
        else:
            flash("Invalid phone and/or password.", "danger")
            return render_template("login.html", form=form)
    return render_template("auth/login.html", form=form)




@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
    # code to validate and add user to database goes here
        name = form.name.data
        age = form.age.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data
        cpassword = form.cpassword.data

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(name=name, age=age, address=address, phone=phone, email=email, password=password)
        new_user.set_password(password)

    # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

#        login_user(new_user)
        flash("Your user has been created, please login.", category="success")
        return redirect(url_for('.login'))
    return render_template('auth/signup.html', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("food.home"))
