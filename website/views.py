from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Bilanz, Buchungssatz, User
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)



@views.route('/kontoerfassung/', methods=['GET', 'POST'])
@login_required
def kontoerfassung():
    if request.method == 'POST':
        bilanz = request.form
        bilanz_name = request.form.get('bilanz_name')
        bilanz_anfangsbestand = request.form.get('bilanz_anfangsbestand')
        bilanz_kontoart = request.form.get('bilanz_kontoart')

        if len(bilanz) != 3:
            flash('Bitte fülle alle Felder aus.', category='error')
        else:
            for sign in """,.:;*+~#'?^°!"$"<>|%&/()=§\][{´`""":
                if bilanz_name.__contains__(sign) or len(bilanz_name) == 0:
                    flash('Bitte keine Satzzeichen in Name eingeben oder leer lassen.', category='error')
                else:
                    continue
            if bilanz_kontoart == 'ertrag' or bilanz_kontoart == 'aufwand' or bilanz_anfangsbestand == '':
                bilanz_anfangsbestand = 0
            new_bilanz = Bilanz(name=bilanz_name, anfangsbestand=bilanz_anfangsbestand, kontoart=bilanz_kontoart,
                                user_id=current_user.id)
            db.session.add(new_bilanz)
            db.session.commit()
            flash('Bilanz wurde hinzugefügt', category='success')

    return render_template("kontoerfassung.html", user=current_user)


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
                    new_buchungssatz = Buchungssatz(wert=buchungssatz_wert, anmerkung=buchungssatz_anmerkung,
                                                    soll_id=buchungssatz_soll, haben_id=buchungssatz_haben,
                                                    user_id=current_user.id)
                    db.session.add(new_buchungssatz)
                    db.session.commit()
                    print(buchungssatz)
                    flash('Buchungssatz wurde hinzugefügt', category='success')

    return render_template('buchungssatz.html', user=current_user)


@views.route('/bestandskonten/', methods=['GET', 'POST'])
@login_required
def bestandskonten():
    if request.method == 'POST':
        abschliessen()
        summen = []
        for bilanz in current_user.bilanzen:
            summe_soll = 0
            summe_haben = 0
            for buchungssatz in current_user.buchungssaetze:
                if bilanz.id == buchungssatz.soll_id:
                    summe_soll += buchungssatz.wert
                elif bilanz.id == buchungssatz.haben_id:
                    summe_haben += buchungssatz.wert
            if bilanz.kontoart == 'aktiv':
                summe_soll += bilanz.anfangsbestand
            elif bilanz.kontoart == 'passiv':
                summe_haben += bilanz.anfangsbestand
            summen.append([summe_soll, summe_haben])
        return render_template('bestandskonten.html', user=current_user, summen=summen)
    else:
        summen = []
        for bilanz in current_user.bilanzen:
            summe_soll = 0
            summe_haben = 0
            for buchungssatz in current_user.buchungssaetze:
                if bilanz.id == buchungssatz.soll_id:
                    summe_soll += buchungssatz.wert
                elif bilanz.id == buchungssatz.haben_id:
                    summe_haben += buchungssatz.wert
            if bilanz.kontoart == 'aktiv':
                summe_soll += bilanz.anfangsbestand
            elif bilanz.kontoart == 'passiv':
                summe_haben += bilanz.anfangsbestand
            summen.append([summe_soll, summe_haben])
        return render_template('bestandskonten.html', user=current_user, summen=summen)


@views.route('/erfolgskonten/', methods=['GET', 'POST'])
@login_required
def erfolgskonten():
    if request.method == 'POST':
        abschliessen()
        summen = []
        for bilanz in current_user.bilanzen:
            summe_soll = 0
            summe_haben = 0
            for buchungssatz in current_user.buchungssaetze:
                if bilanz.id == buchungssatz.soll_id:
                    summe_soll += buchungssatz.wert
                elif bilanz.id == buchungssatz.haben_id:
                    summe_haben += buchungssatz.wert
            if bilanz.kontoart == 'aufwand':
                summe_soll += bilanz.anfangsbestand
            elif bilanz.kontoart == 'ertrag':
                summe_haben += bilanz.anfangsbestand
            summen.append([summe_soll, summe_haben])
        return render_template('erfolgskonten.html', user=current_user, summen=summen)
    else:
        summen = []
        for bilanz in current_user.bilanzen:
            summe_soll = 0
            summe_haben = 0
            for buchungssatz in current_user.buchungssaetze:
                if bilanz.id == buchungssatz.soll_id:
                    summe_soll += buchungssatz.wert
                elif bilanz.id == buchungssatz.haben_id:
                    summe_haben += buchungssatz.wert
            if bilanz.kontoart == 'aufwand':
                summe_soll += bilanz.anfangsbestand
            elif bilanz.kontoart == 'ertrag':
                summe_haben += bilanz.anfangsbestand
            summen.append([summe_soll, summe_haben])
        return render_template('erfolgskonten.html', user=current_user, summen=summen)


@views.route('/guv/', methods=['GET'])
@login_required
def guv():
    if request.method == 'GET':
        summe_aufwendungen = 0
        summe_ertraege = 0
        for guv_bil in current_user.bilanzen:
            if guv_bil.kontoart == 'guv':
                guv = guv_bil
                for ek_bil in current_user.bilanzen:
                    if ek_bil.name == 'Eigenkapital':
                        ek = ek_bil
                if guv.abschlussbestand == None:
                    for bilanz in current_user.bilanzen:
                        if bilanz.kontoart == 'aufwand':
                            summe_aufwendungen += bilanz.abschlussbestand
                        elif bilanz.kontoart == 'ertrag':
                            summe_ertraege += bilanz.abschlussbestand
                    print(guv.name)
                    print(ek.name)
                    print(guv.abschlussbestand)
                    guv.abschlussbestand = summe_aufwendungen - summe_ertraege
                    db.session.commit()
                else:
                    for bilanz in current_user.bilanzen:
                        if bilanz.kontoart == 'aufwand':
                            summe_aufwendungen += bilanz.abschlussbestand
                        elif bilanz.kontoart == 'ertrag':
                            summe_ertraege += bilanz.abschlussbestand
                    print(guv.name)
                    print(ek.name)
                    print(guv.abschlussbestand)
                    if guv.abschlussbestand < 0:
                        ek_an_guv = Buchungssatz(wert=abs(guv.abschlussbestand), soll_id=ek.id, haben_id=guv.id,
                                                    anmerkung="Eigenkapital an GuV", user_id=current_user.id)
                        db.session.add(ek_an_guv)
                        db.session.commit()
                        guv.abschlussbestand += ek_an_guv.wert
                        db.session.commit()
                        print("ek an guv ", abs(guv.abschlussbestand))
                    elif guv.abschlussbestand > 0:
                        guv_an_ek = Buchungssatz(wert=abs(guv.abschlussbestand), soll_id=guv.id, haben_id=ek.id,
                                                    anmerkung="GuV an Eigenkapital", user_id=current_user.id)
                        db.session.add(guv_an_ek)
                        db.session.commit()
                        guv.abschlussbestand -= guv_an_ek.wert
                        db.session.commit()
                    elif guv.abschlussbestand == 0.0:
                        for buchung in current_user.buchungssaetze:
                            if buchung.soll_id == guv.id and buchung.haben_id == ek.id:
                                summe_ertraege += buchung.wert
                            elif buchung.soll_id == ek.id and buchung.haben_id == guv.id:
                                summe_aufwendungen += buchung.wert
        return render_template('guv.html', user=current_user, summe_aufwendungen=summe_aufwendungen,
                               summe_ertraege=summe_ertraege)


@views.route('/schlussbilanz/', methods=['GET'])
@login_required
def schlussbilanz():
    summe_aufwendungen = 0
    summe_ertraege = 0
    if request.method == 'GET':
        for bilanz in current_user.bilanzen:
            if bilanz.kontoart == 'aktiv':
                summe_aufwendungen += bilanz.abschlussbestand
            elif bilanz.kontoart == 'passiv':
                summe_ertraege += bilanz.abschlussbestand
        return render_template("schlusbilanz.html", user=current_user, summe_aufwendungen=summe_aufwendungen,
                               summe_ertraege=summe_ertraege)


def abschliessen():
    for bilanz in current_user.bilanzen:
        summe_soll = 0
        summe_haben = 0
        bilanz.abgeschlossen = True if bilanz.kontoart != 'guv' else bilanz.abgeschlossen == False
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
        elif bilanz.kontoart == 'aufwand':
            summe_soll += bilanz.anfangsbestand
            bilanz.abschlussbestand = summe_soll - summe_haben
        elif bilanz.kontoart == 'ertrag':
            summe_haben += bilanz.anfangsbestand
            bilanz.abschlussbestand = summe_haben - summe_soll
        db.session.commit()
