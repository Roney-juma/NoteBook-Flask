from flask import render_template,url_for,flash,redirect,request
import pyotp
from . import auth
from flask_login import login_user,login_required,logout_user
from .forms import RegForm,LoginForm
from ..models import User
from .. import db
from ..email import mail_message





@auth.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
      user = User.query.filter_by(email = form.email.data).first()
      if user != None and user.verify_password(form.password.data):
        login_user(user,form.remember.data)
      return redirect(url_for("auth.login_2fa"))
      flash('Invalid username or Password')

    return render_template('auth/login.html', loginform = form)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for("main.index"))

@auth.route('/signup', methods = ["GET","POST"])
def signup():
    form = RegForm()
    if form.validate_on_submit():
      user = User(email = form.email.data, username = form.username.data, password = form.password.data)
      user.save_u()
      mail_message("Welcome to the Quick Note","email/welcome_user",user.email,user=user)
      return redirect(url_for('auth.login'))
    return render_template('auth/rejister.html', r_form = form)

# 2FA page route
@auth.route("/login/2fa/")
def login_2fa():
    # generating random secret key for authentication
    secret = pyotp.random_base32()
    return render_template("auth/login_2fa.html", secret=secret)
 # 2FA form route
@auth.route('/login_2fa/', methods=['POST'])
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
      flash("The TOTP 2FA token is valid", "success")
      return redirect(request.args.get('next') or url_for('blog.index'))