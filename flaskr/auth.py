import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

#: Create a blueprint named auth, located at current module and prepend /auth to all url:s associated
bp = Blueprint('auth', __name__, url_prefix='/auth')


#: Function runs before all view-functions in bp
@bp.before_app_request
#: Stores user-data on g until end of request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


#: This is a decorator, it wraps the view supplied
#: If g.user is not defined, redirect to log in, else render supplied view
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


#: Associates the specified route with view
@bp.route('/register', methods=('GET', 'POST'))
#: Defines a view?
def register():
    if request.method == 'POST':
        #: request.form is some sort of magic to extract value from form
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        #: error is for storing messages for user
        error = None

        #: Bad validation of form
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                #: execute takes sql with ? placeholders and tuple to fill, built in sql inj protection
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    #: hashing of pass from werkzeug which comes with flask
                    (username, generate_password_hash(password)),
                )
                #: commit must be run to save changes to data?
                db.commit()
            #: Why is this a specified error? Are there no other errors?
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                #: Returns a redirection response to login view
                return redirect(url_for("auth.login"))

        #: error is saved and can be retrieved when template is rendered?
        flash(error)
    #: Will render the doc specified
    return render_template('auth/register.html')


#: See /register route for comments in common
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        #: Where is the form validation?
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            #: Session stores a signed cookie with the info of userId
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


#: Clears user from cookie
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))