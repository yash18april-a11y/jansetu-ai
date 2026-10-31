import pytest
from app import create_app
from app.extensions import db
from app.models import Scheme

@pytest.fixture
def client():
    app=create_app({'TESTING':True,'SQLALCHEMY_DATABASE_URI':'sqlite:///:memory:','JWT_SECRET_KEY':'jansetu-automated-testing-secret-key-2026-only'})
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove();db.drop_all()

def test_auth_and_profile(client):
    assert client.post('/api/auth/register',json={'email':'person@example.com','password':'secure-pass-123'}).status_code==201
    token=client.post('/api/auth/login',json={'email':'person@example.com','password':'secure-pass-123'}).json['access_token']
    headers={'Authorization':f'Bearer {token}'}
    assert client.put('/api/profile',headers=headers,json={'age':21,'state':'Madhya Pradesh'}).status_code==200
    assert client.get('/api/profile',headers=headers).json['age']==21
    assert client.get('/api/schemes').json==[]

def test_unauthorized(client):
    assert client.get('/api/profile').status_code==401

