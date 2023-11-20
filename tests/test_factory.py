from flaskr import create_app
#: Most factory code will run each test and thus be tested


#: Tests for possibility of changing testing-status
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


#: Tests response data of hello-route
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
