from flask import render_template, redirect,url_for,abort,request,flash
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
@login_required
def index():
    notes = Note.query.order_by(Note.time.desc())
    return render_template('index.html', notes=notes)

@main.route('/note/<id>')
@login_required
def note(id):
    note = Note.query.get(id)
    return render_template('note.html',note=note)

@main.route('/new_note', methods=['POST','GET'])
@login_required
def new_note():
    subscribers = Subscriber.query.all()
    form = CreateNote()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        user_id =  current_user._get_current_object().id
        note = Note(title=title, content=content,category=category,user_id=user_id)
        note.save()
        for subscriber in subscribers:
            mail_message("New note created","email/new_note",subscriber.email,note=note)
        return redirect(url_for('main.index'))
    return render_template('add_note.html', form = form)

@main.route('/note/<note_id>/update', methods = ['GET','POST'])
@login_required
def updatenote(note_id):
    note = Note.query.get(note_id)
    if note.user != current_user:
        abort(403)
    form = CreateNote()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        category = form.category.data

        db.session.commit()
        return redirect(url_for('main.note',id = note.id)) 
    if request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
        form.category = form.category.data

    return render_template('edit_note.html', form = form)

@main.route('/note/<note_id>/delete', methods = ['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note.user != current_user:
        abort(403)
    note.delete()
    return redirect(url_for('main.index'))

@main.route('/to_do_list')
def toDoList():
    todo = Note.query.filter_by(category = 'To do list').all() 
    return render_template('to_do_list.html', todo = todo)

@main.route('/to_recall_list')
def toRecallList():
    torecall = Note.query.filter_by(category = 'Items to remember').all()
    return render_template('to_recall.html', torecall = torecall)

@main.route('/online_resource')
def online():
    online = Note.query.filter_by(category = 'Online resources').all()
    return render_template('online.html', online = online)

@main.route('/general')
def general():
    general = Note.query.filter_by(category = 'General').all()
    return render_template('general.html', general = general)

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to Quick Notes","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    return redirect(url_for('main.index'))

@main.route('/profile/<name>',methods = ['POST','GET'])
@login_required
def profile(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return render_template('profile/profile.html',user = user)
 
@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    user = User.query.filter_by(username = name).first()
    form = UpdateProfile()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('main.profile',name=user.username,))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    return render_template('profile/update.html', user = user, form =form)

@main.route('/profile/<username>/update/pic',methods= ['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

        flash('User pic updated')
        
    return redirect(url_for('main.update_profile',username=username))

