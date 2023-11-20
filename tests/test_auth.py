import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    #: Asserts res on GET
    assert client.get('/auth/register').status_code == 200
    #: Asserts reroute on post req with valid data
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        #: Asserts user has been registered
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


#: Runs same test with different prams
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
    #: To compare text use get_data(as_text=True), res.data is in bytes


#: Tests login route
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    #: Logs in by using function in config?
    response = auth.login()
    assert response.headers["Location"] == "/"

    #: Keeps client accessible after res is returned
    with client:
        client.get('/')
        #: Tests g which is used for authentication in client?
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
