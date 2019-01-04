from flask import render_template, flash, redirect, url_for, request, jsonify, json
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Person
from app import app, db
from app.forms import LoginForm, RegistrationForm, SettingsForm, UpdateEmailForm, UpdatePasswordForm
import os



user_id_dict = {
    "1": "Kwasi",
    '2': "Gene",
    '3': "Carter",
    '4': "Kenso"
}



#TODO: display subjectImg and subjectName for each unique user_id (subkect)
# add name under user image
# fix url issue with subjectName
#
@app.route('/')
@app.route('/index')
@login_required
def index():
    moodQuery=Person.query.filter_by(user_id=1).all()
    moodSum = 0
    moodAverage = 0
    subjectId = moodQuery
    subjectName = ''
    if len(moodQuery) > 0:
        subjectName = user_id_dict[str(moodQuery[0])]

    #To check if folder exists, create if doesnt exists
    exist_path = os.path.join('snapShots', subjectName)
    if os.path.exists(exist_path):
        subjectImg = os.path.join('snapShots', subjectName, '{}.jpg'.format(subjectName))
    else:
        os.mkdir('snapShots', subjectName)

    for i in range(len(moodQuery)):
        moodSum += moodQuery[i].mood
        moodAverage += (moodSum/(len(moodQuery)))
    impath = "/static/snapShots/{}/{}.jpg".format(subjectName, subjectName)
    return render_template('index.html', title='Home', mood= moodAverage, subjectImg = subjectImg, subjectName = subjectName, impath=impath)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)






@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/settings')
@login_required
def settings():
    form = SettingsForm()
    return render_template('settings.html', title='Settings', form = form)


@app.route('/update_password', methods =['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        #The checking of the password hash won't work here. Will prompt error message even upon successful change of password
        if not check_password_hash(current_user.password_hash, form.current_password.data):
            flash('This is not your current password')
        if form.new_password2.data != form.new_password.data:
            flash('New passwords do not match')

        new_pass = current_user.set_password(form.new_password2.data)

        db.session.commit()
        flash('Password succesfully updated!')
        return redirect(url_for('index'))

    return render_template('update_password.html', title ='Update Password', form = form)


@app.route('/update_email', methods=['GET','POST'])
@login_required
def update_email():
    form = UpdateEmailForm()
    if form.validate_on_submit():
        if form.current_email.data != current_user.email:
            flash('Incorrect current email!')
        if form.new_email2.data != form.new_email.data:
            flash('New emails do not match!')
        current_user.email = form.new_email2.data
        db.session.commit()
        flash('Email succesfully updated')
        return redirect(url_for('index'))
 #   flash('An error has occure while attempting to update email.')
#    return redirect(url_for('update_email'))
    return render_template('update_email.html', title = 'Update Email', form= form)

