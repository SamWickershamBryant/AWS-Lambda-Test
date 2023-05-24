from app import app as chalice_app
import pytest
from chalice import Chalice
from http import HTTPStatus
import json

@pytest.fixture
def app() -> Chalice:
    return chalice_app

def test_index(client):
    response = client.get('/')
    assert response.json == {'hello': 'world'}
    assert response.status_code == HTTPStatus.OK

def test_list_all(client):
    response = client.get('/metalbands')
    
    assert response.status_code == HTTPStatus.OK

def test_add(client):
    response = client.post(
        '/add',
        headers={'Content-Type':'application/json'},
        body=json.dumps({'origin':'mom','formed':'1999','split':'-','band_name':'sams','id':'1','fans':'69','style':'cool'})
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"status": "success"}

def test_delete(client):
    response = client.get('/delete/1')
    response2 = client.get('/delete/1')
    assert response.status_code == HTTPStatus.OK
    assert response2.status_code == HTTPStatus.BAD_REQUEST

def test_query(client):
    response = client.get('/query/split/1999')
    response2 = client.get('/query/wrong/404')
    assert response.status_code == HTTPStatus.OK or response.status_code == HTTPStatus.NOT_FOUND
    assert response2.status_code == HTTPStatus.BAD_REQUEST

def test_update(client):
    response = client.put(
        '/update',
        headers={'Content-Type':'application/json'},
        body=json.dumps({'origin':'da basement','formed':'1899','split':'-','band_name':'jim','id':'100','fans':'699','style':'coolness'})
    )
    response2 = client.put(
        '/update',
        headers={'Content-Type':'application/json'},
        body=json.dumps({'formed':'1899','split':'-','band_name':'jim','id':'100','fans':'699','style':'coolness'})
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"status": "success"}
    assert response2.status_code == HTTPStatus.BAD_REQUEST

