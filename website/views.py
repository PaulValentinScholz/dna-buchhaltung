from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Bilanz, Buchungssatz
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        bilanz = request.form
        bilanz_name = request.form.get('bilanz_name')
        bilanz_anfangsbestand = request.form.get('bilanz_anfangsbestand')
        bilanz_kontoart = request.form.get('bilanz_kontoart')

        if len(bilanz) != 3:
            flash('Bitte fülle alle Felder aus.', category='error')
        else:
            if bilanz_name.__contains__(""",.:;*+~#'?^°!"$%&/()=§\][{´`""") or len(bilanz_name) == 0:
                    flash('Bitte keine Satzzeichen in Name eingeben oder leer lassen.', category='error')
            else:
                if bilanz.kontoart == 'ertrag' or bilanz.kontoart == 'aufwand':
                    bilanz_anfangsbestand = 0
                new_bilanz = Bilanz(name=bilanz_name, anfangsbestand=bilanz_anfangsbestand, kontoart=bilanz_kontoart, user_id=current_user.id)
                db.session.add(new_bilanz)
                db.session.commit()
                
                flash('Bilanz wurde hinzugefügt', category='success')    
    return render_template("bilanz.html", user=current_user) 


@views.route('/buchungssatz/', methods=['GET', 'POST'])
@login_required
def buchungssatz():
    if request.method == 'POST':
        buchungssatz = request.form
        buchungssatz_soll = request.form.get('buchungssatz_soll')
        buchungssatz_haben = request.form.get('buchungssatz_haben')
        buchungssatz_wert = request.form.get('buchungssatz_wert')
        buchungssatz_anmerkung = request.form.get('buchungssatz_anmerkung')

        if len(buchungssatz) != 4:
                flash('Bitte fülle alle Felder aus.', category='error')
        else:
            if buchungssatz_wert.__contains__(" ") or len(buchungssatz_wert) == 0:
                    flash('Bitte keine Lehrzeichen in Wert eingeben oder lehr lassen.', category='error')
            else:
                if buchungssatz_soll == buchungssatz_haben:
                    flash('Bitte wähle unterschiedliche Konten aus.', category='error')
                else:
                    new_buchungssatz = Buchungssatz(wert=buchungssatz_wert, anmerkung=buchungssatz_anmerkung, soll_id=buchungssatz_soll, haben_id=buchungssatz_haben, user_id=current_user.id)
                    db.session.add(new_buchungssatz)
                    db.session.commit()
                    print(buchungssatz)
                    flash('Buchungssatz wurde hinzugefügt', category='success')    

    return render_template('buchungssatz.html', user=current_user)

@views.route('/bestandskonten/', methods=['GET', 'POST'])
@login_required
def bestandskonten():
    if request.method == 'POST':
        summen = []
        for bilanz in current_user.bilanzen:
            summe_soll = 0
            summe_haben = 0
            bilanz.abgeschlossen = True
            for buchungssatz in current_user.buchungssaetze:
                if bilanz.id == buchungssatz.soll_id:
                    summe_soll += buchungssatz.wert
                elif bilanz.id == buchungssatz.haben_id:
                    summe_haben += buchungssatz.wert
            if bilanz.kontoart == 'aktiv':
                summe_soll += bilanz.anfangsbestand
                bilanz.abschlussbestand = summe_soll - summe_haben
            elif bilanz.kontoart == 'passiv':
                summe_haben += bilanz.anfangsbestand
                bilanz.abschlussbestand = summe_haben - summe_soll
            summen.append([summe_soll, summe_haben])
            db.session.commit()
        return render_template('bestandskonten.html', user=current_user, summen=summen)
    return render_template('bestandskonten.html', user=current_user)


@views.route('/erfolgskonten/', methods=['GET', 'POST'])
@login_required
def erfolgskonten():
    if request.method == 'POST':
        summen = []
        for bilanz in current_user.bilanzen:
            summe_soll = 0
            summe_haben = 0
            bilanz.abgeschlossen = True
            for buchungssatz in current_user.buchungssaetze:
                if bilanz.id == buchungssatz.soll_id:
                    summe_soll += buchungssatz.wert
                elif bilanz.id == buchungssatz.haben_id:
                    summe_haben += buchungssatz.wert
            if bilanz.kontoart == 'aufwand':
                summe_soll += bilanz.anfangsbestand
                bilanz.abschlussbestand = summe_soll - summe_haben
            elif bilanz.kontoart == 'ertrag':
                summe_haben += bilanz.anfangsbestand
                bilanz.abschlussbestand = summe_haben - summe_soll
            summen.append([summe_soll, summe_haben])
            db.session.commit()
        return render_template('erfolgskonten.html', user=current_user, summen=summen)
    return render_template('erfolgskonten.html', user=current_user)


@views.route('/eroeffnungsbilanz/', methods=['GET', 'POST'])
@login_required
def eroeffnungsbilanz():
    if request.method == 'GET':
        pass
    return render_template('eroeffnungsbilanz.html', user=current_user)
