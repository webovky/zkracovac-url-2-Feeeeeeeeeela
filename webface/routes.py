from . import app
from flask import render_template, request, session, redirect, url_for, g
from os import urandom
from pony.orm import db_session
from . models import User
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
def index():
    title = 'Index'
    return render_template('base.html.j2', title=title, user=session.get("user"))

@app.route('/info/')
def info():
    title = 'Info'
    return render_template('info.html.j2', title=title)

@app.route('/Květák')
def kvetak():
    if g.user:
        title = 'Květák'
        return render_template('kvetak.html.j2', title=title)
    return redirect(url_for('login'))

@app.route('/Kapusta')
def kapusta():
    if g.user:
        title = 'Kapusta'
        return render_template('kapusta.html.j2', title=title)
    return redirect(url_for('login'))

@app.route('/Banány')
def banany():
    if g.user:
        title = 'Banány'
        return render_template('banany.html.j2', title=title)
    return redirect(url_for('login'))

@app.route('/Kalkulačka', methods=["GET", "POST"])
def formulky():
    if g.user:
        label = request.form.get("text")
        if label:
            try:
                result = eval(label)
            except:
                result = "Error :)"
        else:
            result = ""
        title = 'Kalkulačka'
        return render_template('formula.html.j2', title=title, result=result)
    return redirect(url_for('login'))


app.secret_key = urandom(24)

@app.route('/login', methods=["GET", "POST"])
@db_session
def login():
    title = 'login'
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.get(login=username)
        if user:
            if check_password_hash(user.password, password):
                session["user"] = user.login
                return redirect(url_for("index"))
            else:
                return render_template('login.html.j2', title=title, error="Špatný heslo kolego")

        else:
            return render_template('login.html.j2', title=title, error="Špatný jméno kolego")


    return render_template('login.html.j2', title=title)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/')
def dropsession():
    session.pop('user', None)
    return render_template('login.html.j2')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html.j2')

@app.route("/register", methods=["GET","POST"])
@db_session
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        existing = User.get(login=username)
        if username and not existing and password == password2:
            user = User(login=username,password=generate_password_hash(password))
            session["user"] = user.login
            return redirect(url_for("index"))
        else:
            return render_template("register.html.j2", error="Máš tam chybu")

    return render_template("register.html.j2")

@app.route("/logout")
def logout():
    g.user = None
    session["user"] = ""
    return redirect(url_for("index"))

@app.route("/short", methods=["GET","POST"])
def short():
    pass
