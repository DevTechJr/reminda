from . import db, admin
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     notes = db.relationship('User')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class UsersView(ModelView):
    pass

admin.add_view(UsersView(User, db.session))

class Sighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    location = db.Column(db.String(350))
    time = db.Column(db.DateTime(timezone=True), default=func.now())

class SightingView(ModelView):
    pass

admin.add_view(SightingView(Sighting, db.session))

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    picture = db.Column(db.String(550))
    relation = db.Column(db.String(150))
    summary = db.Column(db.String(150))
    specialMemory = db.Column(db.String(550))

class PeopleView(ModelView):
    pass

admin.add_view(PeopleView(People, db.session))

    
