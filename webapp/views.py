import json
from flask import render_template, flash, redirect, request, url_for, jsonify, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from . models import db, User, Images, Albums

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    photos = 0
    if current_user.albums:
        photos = len([img for album in current_user.albums for img in album.imgs])
    return render_template('home.html', photos=photos)

@views.route('/albums')
@login_required
def albums():
    albums = current_user.albums
    return render_template('albums.html', albums=albums)

@views.route('/create_album', methods=['POST'])
@login_required
def create_album():
    if request.method == 'POST':
        name = request.form['name']
        pin1 = request.form['pin-1']
        pin2 = request.form['pin-2']
        pin3 = request.form['pin-3']
        pin4 = request.form['pin-4']
        pin = pin1 + pin2 + pin3 + pin4
        user_id = current_user.id
        if not Albums.query.filter_by(name=name).first():
            album = Albums(name=name, pin=pin, user_id=user_id)
            db.session.add(album)
            db.session.commit()
        else:
            flash('Album name already exists!')
        return redirect(url_for('views.albums'))

@views.route('/delete_album', methods=['POST'])
@login_required
def delete_album():
    if request.method == 'POST':
        id = json.loads(request.data).get('id')
        if id:
            album = Albums.query.get(int(id))
            if album:
                album = db.session.merge(album)
                db.session.delete(album)
                db.session.commit()
            return jsonify({})

@views.route('/upload_pic', methods=['POST'])
@login_required
def upload_pic():
    pic = request.files['picture']
    album_id = request.form['id']
    if not pic:
        flash('No picture to upload!')
        return redirect(url_for('views.get_images', id=album_id))
    else:
        filename = secure_filename(pic.filename)
        img = Images(img=pic.read(), name=filename, album_id=album_id)
        db.session.add(img)
        db.session.commit()
    return redirect(url_for('views.get_images', id=album_id))

@views.route('/get_pin', methods=['POST'])
@login_required
def get_pin():
    if request.method == 'POST':
        id = json.loads(request.data).get('id')
        albums = current_user.albums
        for album in albums:
            if int(id) == album.id:
                return jsonify(album.pin)
        return 400

@views.route('/images/<id>')
@login_required
def get_images(id):
    albums = current_user.albums
    for album in albums:
        if int(album.id) == int(id):
            return render_template('images.html', album=album)
    return redirect(url_for('views.albums'))

@views.route('/delete_img/<id>', methods=['POST'])
@login_required
def delete_img(id):
    if id:
        img = Images.query.get(int(id))
        img = db.session.merge(img)
        db.session.delete(img)
        db.session.commit()
        return jsonify({})

@views.route('/account')
@login_required
def account():
    return render_template('account.html')

@views.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        _user = User.query.get(current_user.id)
        _user.name = ' '.join([request.form['first_name'], request.form['last_name']])
        _user.email = request.form['email']
        _user.phone = request.form['phone']
        _user.address = request.form['address']
        passw_1 = request.form['password_1']
        passw_2 = request.form['password_2']
        if passw_1 and passw_2:
            if passw_1 == passw_2:
                if len(passw_1) > 7 or len(passw_2):
                    _user.password = generate_password_hash(password=passw_1, method='sha256')
                else:
                    flash("Password too short, must be more than 7 chars")
                    return redirect(url_for('views.account'))
            else:
                flash("Passwords don't match, please verify")
                return redirect(url_for('account'))
        db.session.merge(_user)
        db.session.commit()
        flash('Updated!', 'success')
    return redirect(url_for('views.account'))

@views.route('/update_profile_image', methods=['POST'])
@login_required
def update_profile_image():
    if request.method == 'POST':
        pic = request.files['picture']
    if not pic:
        flash('No image to upload!')
    else:
        _user = User.query.get(current_user.id)
        _user.photo = pic.read()
        db.session.merge(_user)
        db.session.commit()
    return redirect(url_for('views.account'))




