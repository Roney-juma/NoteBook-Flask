from enum import unique
from flask_sqlalchemy.model import Model
from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

class User(UserMixin,db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255),unique = True,nullable = False)
  email  = db.Column(db.String(255),unique = True,nullable = False)
  secure_password = db.Column(db.String(255),nullable = False)
  bio = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String())
  blogs = db.relationship('Blog', backref='user', lazy='dynamic')
  comment = db.relationship('Comment', backref='user', lazy='dynamic')


  @property
  def set_password(self):
    raise AttributeError('You cannot read the password attribute')

  @set_password.setter
  def password(self, password):
    self.secure_password = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.secure_password,password) 
  
  def save_u(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  def __repr__(self):
    return f'User {self.username}'
