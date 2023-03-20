from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Erfolgreich eingelogt!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.bilanzuebersicht'))
            else:
                flash('Falsches Passwort, bitte versuche es erneut.', category='error')
        else:
            flash('Diese Email ist nicht registriert.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Diese Email ist bereits registriert.', category='error')
        elif len(email) < 4:
            flash('Die Email muss mindestens 4 Zeichen enthalten.', category='error')
        elif len(name) <= 2:
            flash('Der Name muss mindestens 3 Zeichen enthalten.', category='error')
        elif password1 != password2:
            flash('Die Passwörter stimmen nicht überein.', category='error')
        elif len(password1) < 7:
            flash('Das Passwort muss mindestens 7 Zeichen lang sein.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), name=name)
            # add user to database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Dein Account wurde erfolgreich erstellt!', category='success')
            
            return redirect(url_for('views.bilanzuebersicht'))

    return render_template('sign_up.html', user=current_user)
