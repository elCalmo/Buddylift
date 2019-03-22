from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):                                       
    id = db.Column(db.Integer, primary_key=True)                        
    username = db.Column(db.String(64), index=True, unique=True)        
    email = db.Column(db.String(120), index=True, unique=True)
    numberplate = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))                           
    lifts = db.relationship('Lift', backref='driver', lazy='dynamic')   

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    start_loc = db.Column(db.String)
    end_loc = db.Column(db.String)
    seats = db.Column(db.Integer)
    user_id_driving = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Lift {}>'.format(self.id)

class UserLift(db.Model):
    userliftId = db.Column(db.Integer, primary_key=True)
    liftId = db.Column(db.Integer, db.ForeignKey('lift.id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))