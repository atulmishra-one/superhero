from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import redirect
from flask import send_file
from flask import jsonify
from flask import abort

from forms import UserLoginForm
from forms import get_user
from forms import MemberForm
from forms import SubscriptionsForm
from flask_login import login_required, login_user, logout_user, current_user

from models import UserType
from models import User
from models import Subscriptions
from models import UserPage

from io import BytesIO

from scripts import get_php

import subprocess
import requests


def index():
    form = UserLoginForm(request.form)

    if request.method == 'POST':
        user = get_user(form.email.data, form.password.data)
        if form.validate():
            user_type = UserType.query.get(user.user_type)
            session['user_info'] = dict(
                email=user.email,
                id=user.id,
                password=user.password,
                user_type=user_type.name
            )
            login_user(user, fresh=True)

            if user_type.name == 'thedeft':
                return redirect('bhul_bhulai_ya')
            return redirect('dashboard')
        else:
            flash(form.errors)
            redirect('/')

    return render_template(
        'index.html',
        form=form
    )


@login_required
def dashboard():
    subscriptions = Subscriptions.query\
        .filter(Subscriptions.user_id == current_user.id).all()
    return render_template('dashboard.html', subscriptions=subscriptions)


@login_required
def bhul_bhulai_ya(page=None):

    members = User.query.join(
        UserType, User.user_type == UserType.id
    ).filter(UserType.name != 'thedeft').order_by(User.date_created.desc())

    subscriptions = Subscriptions.query.join(
        User, User.id == Subscriptions.user_id
    ).add_columns(Subscriptions.id, User.email, Subscriptions.active, Subscriptions.user_id)\
        .order_by(Subscriptions.date_created.desc())

    members_form = MemberForm(request.form)
    subscriptionsform = SubscriptionsForm(request.form)
    subscriptionsform.user_email.choices = [(user.id, user.email)
                                            for user in User.query.all()]

    if request.method == 'POST':
        if members_form.validate():
            members_form.save()
            return redirect('bhul_bhulai_ya/members')

        if subscriptionsform.validate():
            subscriptionsform.save()
            return redirect('bhul_bhulai_ya/subscriptions')

    return render_template(
        'bhul_bhulai_ya_dashboard.html',
        page='{}.html'.format(page or 'members'),
        members=members,
        subscriptions=subscriptions,
        members_form=members_form,
        subscriptionsform=subscriptionsform
    )


def download(member_id, subscription_id):
    io = BytesIO()
    io.write(get_php(
        member_id,
        subscription_id
    ))
    io.seek(0)
    return send_file(
        io,
        attachment_filename='superhero_{}_{}.php'.format(member_id, subscription_id),
        as_attachment=True, mimetype='text/plain')


def lab():
    form = request.form
    ip = form['ip']
    boat = False

    subscriptions = Subscriptions.query.filter(
        Subscriptions.user_id == form['user_id'],
        Subscriptions.id == form['id'],
        Subscriptions.active == 1
    ).first()

    if not subscriptions:
        return abort(401)

    money_page, safe_page = False, False

    user_page = UserPage.query.filter(UserPage.user_id == form['user_id']).first()

    user_money_page, user_safe_page = user_page.money_page, user_page.safe_page

    output = subprocess.Popen('host {}'.format(ip), shell=True, stdout=subprocess.PIPE)\
        .communicate()[0]
    if output:
        host1 = str(output).split(' ')[::-1][0].replace('.'"\\n", '').replace("'", '')
        print(host1)
        if host1:
            reverse_lookup = subprocess\
                .Popen("host {}".format(host1), shell=True, stdout=subprocess.PIPE)\
                .communicate()[0]
            reverse_lookup = str(reverse_lookup).split(' ')[0].replace('.'"\\n", '').replace("'", '')[1:]
            print(reverse_lookup)
            if reverse_lookup:
                if host1 == reverse_lookup:
                    if 'googlebot' in reverse_lookup or 'google.com' in reverse_lookup:
                        boat = True
    else:
        boat = False

    safe_page = True
    money_page = False

    if not boat:
        response = requests.get('http://freegeoip.net/json/{}'.format(ip))
        json_data = response.json()

        if json_data['country_code'] == 'US':
            money_page = True
            safe_page = False

    if form['query']:
        user_money_page = '{}?{}'.format(user_money_page, form['query'])
        user_safe_page = '{}?{}'.format(user_safe_page, form['query'])

    return jsonify(results=[
        dict(
            safe_page=safe_page,
            money_page=money_page,
            user_money_page=user_money_page,
            user_safe_page=user_safe_page
        )
    ])



