import pytest
from flask import Flask

@pytest.fixture
def client(app: Flask):
    return app.test_client()

def test_example(client):
    response = client.get('/')
    assert response.status_code == 200
