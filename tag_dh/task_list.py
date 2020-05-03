from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)

from tag_dh import db
from tag_dh.models import Task, Account

bp = Blueprint('task_list', __name__)

@bp.route('/tasks', methods=('GET', 'POST'))
def index():
    if not session.get('validUser', False):
        return redirect(url_for('task_list.login'))

    if request.method == 'POST':
        name = request.form['name']
        if not name:
            flash('Task name is required.', username)
        else:
            db.session.add(Task(name=name))
            db.session.commit()
        return redirect(url_for('task_list.index'))

    tasks = Task.query.all()
    return render_template('task_list/index.html', tasks=tasks)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        chk_password = request.form["chk_password"]
        if password != chk_password:
            flash("The passwords don't match")
            return redirect(url_for('task_list.signup'))
        else:
            db.session.add(Account(user=username, pwrd=password))
            db.session.commit()
            session['validUser'] = True
            session['username'] = username
            flash("Account successfully created")
            return redirect(url_for('task_list.index'))

    return render_template('task_list/signup.html')

@bp.route('/login', methods=('GET','POST'))
def login():
    if session.get("validUser", False):
        return redirect(url_for('task_list.index'))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if Account.query.filter_by(user=username).filter_by(pwrd=password).first() == None:
            flash("Incorrect username or password")
            return redirect(url_for('task_list.login'))
        else:
            session['validUser'] = True
            session['username'] = username
            return redirect(url_for('task_list.index'))

    return render_template('task_list/login.html')

@bp.route('/logout', methods=('GET','POST'))
def logout():
    session['validUser'] = False
    flash("You have been logged out.")
    return redirect(url_for('task_list.login'))


@bp.route('/tasks/<int:id>/delete', methods=('POST',))
def delete(id):
    task = Task.query.get(id)
    if task is not None:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('task_list.index'))
