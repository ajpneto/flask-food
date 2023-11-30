from sqlalchemy import desc, func
from flask import render_template, Blueprint, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from datetime import date, datetime, timedelta
from itertools import groupby
from .. import db
from ..auth.models import User
from .models import MenuItem, Order, Rating, Bill, BookTable
import requests, json, ast
from .forms import MenuForm, BookForm
from .. import photos


food_bp = Blueprint(
    'food',
    __name__,
    url_prefix="/"
)

def menu():
    menu_items = MenuItem.query.all()
    items_by_category = {}

    for key, group in groupby(menu_items, key=lambda x: x.category):
        items_by_category[key] = list(group)

    return items_by_category


@food_bp.route('/', methods=['GET', 'POST'])
def home():
    all_reviews = Rating.query.order_by(Rating.r_date.desc()).all()
    items_by_category = menu()
    form = BookForm()
    if form.validate_on_submit():
    # code to validate and add book to database goes here
        name = form.name.data
        phone = form.phone.data
        bdate = form.bdate.data
        btime = form.btime.data
        num_peoples = form.num_peoples.data
        special = form.special.data

    # create a new book with the form data..
        new_book = BookTable(name=name,
                             phone=phone,
                             bdate=bdate,
                             btime=btime,
                             num_peoples=num_peoples,
                             special=special)

    # add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        flash("Recebemos a sua reserva, obrigado!.", category="success")
        return redirect(url_for('.home'))
    return render_template('index.html', items_by_category=items_by_category, all_reviews=all_reviews, form=form)


@food_bp.route('/offers')
def offers(request):
    return render_template('offers.html')


@food_bp.route('/reviews', methods=['GET','POST'])
def reviews():
    if request.method == 'POST':
        if current_user.is_authenticated:
            name = current_user.name
            phone = current_user.phone
        else:
            name = 'Unknow'
            phone = 'Unknow'
        cmt = request.form.get('comment')
        date_now = datetime.now()

        review = Rating(name=name,
                        comment=cmt,
                        r_date=date_now)
        db.session.add(review)
        db.session.commit()

    all_reviews = Rating.query.order_by(Rating.r_date.desc()).all()

    return render_template('reviews.html', all_reviews=all_reviews)


@food_bp.route('/profile')
@login_required
def profile():
    if not current_user.is_authenticated:
        flash('Por favor, faça login.', category='warning')
        return redirect(url_for('auth.login'))
    return render_template('profile.html')


@food_bp.route('/manage_menu', methods=['GET', 'POST'])
@login_required
def manage_menu():
    form = MenuForm()
    if form.validate_on_submit():
        image_url = photos.save(form.pic.data)

        new_dish = MenuItem(name=form.name.data, category=form.category.data, price=form.price.data,
                              desc=form.desc.data, pic="/static/uploads/" + image_url)

        db.session.add(new_dish)
        db.session.commit()

        flash('Novo prato adicionado!', category='success')
        return redirect(url_for('.home'))

    return render_template('manage_menu.html', admin=True, form=form)



@food_bp.route('/delete_dish/<int:item_id>',  methods=['GET', 'POST'])
def delete_dish(item_id):
    product = MenuItem.query.get_or_404(item_id)
    db.session.delete(product)
    db.session.commit()
    flash('O produto foi removido com sucesso', category="info")
    return redirect(url_for('.home'))



@food_bp.route('/cart', methods=['GET','POST'])
def cart():

    if request.method == 'POST':
        if current_user.is_authenticated:
            name = current_user.name
            phone = current_user.phone
        else:
            name = 'Unknow'
            phone = 'Unknow'
        items_json = request.form.get('items_json')
        table_number = request.form.get('table_value')
        total = request.form.get('price')
        print(total)

        now = datetime.now()
#        now_ist = now + timedelta(hours=5, minutes=30)

        if table_number == 'null':
            table_number = 'Take Away'

        new_order = Order(name=name,
                          phone=phone,
                          items_json=items_json,
                          table=table_number,
                          order_time=now,
                          price=total)
        db.session.add(new_order)
        db.session.commit()

    return render_template('cart.html')


@food_bp.route('/my_orders')
@login_required
def my_orders():

    phone = current_user.phone

    orders = Order.query.filter_by(phone=phone)
    order_by_table = {}

    for key, group in groupby(orders, key=lambda x: x.table):
        order_by_table[key] = list(group)
    for table, orders in order_by_table.items():
        for ord in orders:
            items_json_str = ord.items_json
            ord.items_json = json.loads(items_json_str)


    return render_template('my_orders.html', order_by_table=order_by_table)


@food_bp.route('/all_orders')
def all_orders():

    orders = Order.query.order_by(Order.order_time.desc()).all()
    order_by_table = {}

    for key, group in groupby(orders, key=lambda x: x.table):
        order_by_table[key] = list(group)

    for table, orders in order_by_table.items():
        for ord in orders:
            items_json_str = ord.items_json
            ord.items_json = json.loads(items_json_str)


    return render_template('all_orders.html', order_by_table=order_by_table)


@food_bp.route('/generate_bill')
def generate_bill():
    t_number = request.args.get('table')

    order_for_table = Order.query.filter_by(table=t_number, bill_clear=False)
    bill_total = 0
    now = datetime.now()
#    now_ist = now + timedelta(hours=5, minutes=30)

    bill_items = []
    c_name = ''
    c_phone = ''
    for o in order_for_table:
        bill_total += int(o.price)
        o.bill_clear = True
        db.session.add(o)
        db.session.commit()

        bill_items.append({
            'order_items': o.items_json,
        })
        c_name = o.name
        c_phone = o.phone

    order_dict = {}
    for item in bill_items:
        for key, value in item.items():
            order_items = json.loads(value)
            for pr_key, pr_value in order_items.items():
                order_dict[pr_value[1].lower()] = [
                    pr_value[0], (int(pr_value[2]) * int(pr_value[0]))
                ]
    new_bill = Bill(order_items=str(order_dict),
                    name=c_name,
                    bill_total=bill_total,
                    phone=c_phone,
                    bill_time=now)
    db.session.add(new_bill)
    db.session.commit()


    return render_template('generate_bill.html', order_dict=order_dict,
        bill_total=bill_total,
        c_name=c_name,
        c_phone=c_phone,
        bill_id=new_bill.bill_id
)


@food_bp.route('/view_bills')
def view_bills():

    if not current_user.is_authenticated:
        flash('You Must be an admin user to view this!', category='warning')
        return redirect(url_for('.home'))

    all_bills = Bill.query.order_by(Bill.bill_time.desc()).all()

    for b in all_bills:
        b.order_items = ast.literal_eval(b.order_items)


    return render_template('bills.html', all_bills=all_bills)
