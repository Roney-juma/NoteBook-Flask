from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,TextAreaField,SelectField, SubmitField,ValidationError
from wtforms.validators import Required,Email
from flask_login import current_user
from ..models import User

class UpdateProfile(FlaskForm):
  username = StringField('Enter Your Username', validators=[Required()])
  email = StringField('Email Address', validators=[Required(),Email()])
  bio = TextAreaField('Write a brief bio about you.',validators = [Required()])
  submit = SubmitField('Update')

  def validate_email(self,email):
    if email.data != current_user.email:
      if User.query.filter_by(email = email.data).first():
        raise ValidationError("The Email has already been taken!")
    
  def validate_username(self, username):
    if username.data != current_user.username:
      if User.query.filter_by(username = username.data).first():
        raise ValidationError("The username has already been taken")

class CreateNote(FlaskForm):
  title = StringField('Title',validators=[Required()])
  content = TextAreaField('Note Content',validators=[Required()])
  category = SelectField('Category', choices=[('To do list','To do list'),('Items to remember','Items to remember'),('Online resources','Online resources'),('General','General')],validators=[Required()])

  submit = SubmitField('Add')