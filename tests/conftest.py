import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


#: Fixtures are used by each test
@pytest.fixture
def app():
    #: Creates temporary file and returns path and descriptor
    db_fd, db_path = tempfile.mkstemp()

    #: Database path and testing status is overridden
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    #: Temp database is reset
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
#: Client fixture simulates client to send requests without starting server
def client(app):
    return app.test_client()


@pytest.fixture
#: Runner fixture can call Click commands
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    #: Adds client to auth-object?
    def __init__(self, client):
        self._client = client

    #: Uses added client to log in with username defined in test database file
    def login(self, username='test', password='test'):
        #: Returns post request to log in endpoint
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


#: Fixture can be used to log in / log out client while testing
@pytest.fixture
def auth(client):
    return AuthActions(client)