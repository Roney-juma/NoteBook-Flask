from flask import render_template, redirect,url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Note,Subscriber
from ..import db, photos
import secrets
import os
from PIL import Image
from .forms import UpdateProfile,Createnote
from ..email import mail_message

#Views
@main.route('/')
def index():
    notes = Note.query.order_by(Note.time.desc())
    return render_template('notes_page.html', notes=notes)