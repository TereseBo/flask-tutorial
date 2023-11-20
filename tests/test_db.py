import sqlite3
import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        #: Same db connection should be returned inside same context
        db = get_db()
        assert db is get_db()

    #: Checks message if running command after close
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

    #: The init_db command should init db
    #: Runner fixture is used to run init-db command
    #: Monkeypatch fixture replaces init_db function
    def test_init_db_command(runner, monkeypatch):
        class Recorder(object):
            called = False

        def fake_init_db():
            Recorder.called = True

        #: Replaces command response?
        monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
        #: Sets result to invocation of init_db
        result = runner.invoke(args=['init-db'])
        #: Asserts initialization
        assert 'Initialized' in result.output
        #: Asserts actual running of faked function
        assert Recorder.called
