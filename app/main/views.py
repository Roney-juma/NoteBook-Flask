from flask import render_template, redirect,url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Note,Subscriber
from ..import db, photos
import secrets
import os
from PIL import Image
from .forms import UpdateProfile,CreateNote
from ..email import mail_message

#Views
@main.route('/')
def index():
    notes = Note.query.order_by(Note.time.desc())
    return render_template('notes_page.html', notes=notes)

@main.route('/new_note', methods=['POST','GET'])
@login_required
def new_note():
    subscribers = Subscriber.query.all()
    form = CreateNote()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id =  current_user._get_current_object().id
        note = Note(title=title, content=content,user_id=user_id)
        note.save()
        for subscriber in subscribers:
            mail_message("New note created","email/new_note",subscriber.email,note=note)
        return redirect(url_for('main.index'))
    return render_template('add_note.html', form = form)