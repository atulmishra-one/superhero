from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserType(db.Model):
    __tablename__ = 'usertype'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.ForeignKey('usertype.id'))
    date_created = db.Column(db.DateTime, default=db.func.now())

    def is_active(self):
        """True, as all users are active."""
        return self.active

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.ForeignKey('user.id'))
    active = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.now())


class UserPage(db.Model):
    __tablename__ = 'userpage'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    money_page = db.Column(db.String(255))
    safe_page = db.Column(db.String(255))
