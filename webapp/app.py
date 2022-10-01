import json
from flask import Flask, render_template, flash, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, current_user
from models import *
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from base64 import b64encode
from user_bp import users

app = Flask(__name__)
app.secret_key = 'random-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

app.register_blueprint(users)
app.jinja_env.globals.update(len=len, bs4enc=b64encode)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@login_required
def home():
    photos = 0
    if current_user.albums:
        photos = len([img for album in current_user.albums for img in album.imgs])
    return render_template('home.html', photos=photos)

@app.route('/albums')
@login_required
def albums():
    albums = current_user.albums
    return render_template('albums.html', albums=albums)

@app.route('/create_album', methods=['POST'])
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
        return redirect(url_for('albums'))

@app.route('/delete_album', methods=['POST'])
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

@app.route('/upload_pic', methods=['POST'])
@login_required
def upload_pic():
    pic = request.files['picture']
    album_id = request.form['id']
    if not pic:
        flash('No picture to upload!')
        return redirect(url_for('get_images', id=album_id))
    else:
        filename = secure_filename(pic.filename)
        img = Images(img=pic.read(), name=filename, album_id=album_id)
        db.session.add(img)
        db.session.commit()
    return redirect(url_for('get_images', id=album_id))

@app.route('/get_pin', methods=['POST'])
@login_required
def get_pin():
    if request.method == 'POST':
        id = json.loads(request.data).get('id')
        albums = current_user.albums
        for album in albums:
            if int(id) == album.id:
                return jsonify(album.pin)
        return 400

@app.route('/images/<id>')
@login_required
def get_images(id):
    albums = current_user.albums
    for album in albums:
        if int(album.id) == int(id):
            return render_template('images.html', album=album, bs4enc=b64encode)
    return redirect(url_for('albums'))

@app.route('/delete_img/<id>', methods=['POST'])
@login_required
def delete_img(id):
    if id:
        img = Images.query.get(int(id))
        img = db.session.merge(img)
        db.session.delete(img)
        db.session.commit()
        return jsonify({})

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/update_profile', methods=['POST'])
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
                    return redirect(url_for('account'))
            else:
                flash("Passwords don't match, please verify")
                return redirect(url_for('account'))
        db.session.merge(_user)
        db.session.commit()
        flash('Updated!', 'success')
    return redirect(url_for('account'))

@app.route('/update_profile_image', methods=['POST'])
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
    return redirect(url_for('account'))


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=8000)




