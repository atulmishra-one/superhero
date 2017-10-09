from random import randint
from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import ValidationError
from models import User
from models import db
from models import Subscriptions

from sqlalchemy.exc import ProgrammingError


def get_user(email, password=False):
    user = User.query \
        .filter(User.email == email).first()
    if not user:
        return False
    if password:
        if user.password == password:
            return user
        else:
            return False
    if user.email == email:
        return user
    return False


class UserLoginForm(Form):
    email = StringField(u'Email', validators=[
        Email(),
        DataRequired()
    ])
    password = PasswordField(u'Password', validators=[
        DataRequired()
    ])

    def validate_email(form, field):
        user = get_user(field.data)
        if not user:
            raise ValidationError("We'are sorry, but that email is not registered.")

    def validate_password(form, field):
        user = get_user(form.email.data, field.data)
        if not user:
            raise ValidationError("We'are sorry, but that password is not valid.")


class MemberForm(Form):
    email = StringField(u'Email', validators=[
        Email(),
        DataRequired()
    ])

    def validate_email(form, field):
        user = get_user(field.data)
        if user:
            raise ValidationError("We'are sorry, but that email has been registered.")

    def save(self):
        user = User(
            email=self.email.data,
            password='{}'.format(randint(1, 30000)),
            active=0,
            user_type=2
        )
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except ProgrammingError as e:
            print(e)
            return False


class SubscriptionsForm(Form):
    user_email = SelectField('User Email', coerce=int)
    active = BooleanField('Status', default=True)

    def save(self):
        subscriptions = Subscriptions(user_id=self.user_email.data, active=self.active.data)
        try:
            db.session.add(subscriptions)
            db.session.commit()
            return True
        except ProgrammingError:
            return False


