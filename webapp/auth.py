from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . models import db, User

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user:
                saved_password = user.password
                if check_password_hash(saved_password, password):
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Wrong password, try again!')
            else:
                flash("Email don't registred")
        return render_template('login.html')
    return redirect(url_for('views.home'))

@users.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
        first_name = ''
        last_name = ''
        email = ''
        number = ''
        if request.method == 'POST':
            first_name = request.form['firstname']
            last_name = request.form['lastname']
            email = request.form['email']
            number = request.form['number']
            password1 = request.form['password']
            password2 = request.form['confirmpassword']
            user = User.query.filter_by(email=email).first()
            if not user:
                if len(password1) > 7 and len(password2) > 7:
                    if password1 == password2:
                        user = User(email=email, password=generate_password_hash(password=password1, method='sha256'), name=first_name+' '+last_name, phone=number)
                        db.session.add(user)
                        db.session.commit()
                        return redirect(url_for('users.login'))
                    else:
                        flash("Passwords don't match!")   
                else:
                    flash('Password too short!')
            else:
                email = ''
                flash('Email already registred!')
        return render_template('register.html', name=first_name, last_name=last_name, email=email, number=number)
    return redirect(url_for('views.home'))

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))