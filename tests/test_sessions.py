from tests.test_users import create_user, delete_user, main_route
import requests
import pytest


def test_create_session(create_user):
    user = create_user.get('user')
    user_id = user.get('id')
    token = 'fakeToken'
    # create the session with real (temporary) user id
    response = requests.post(f'{main_route()}/sessions/{token}/{user_id}').json()
    assert response.get('status') == 'OK'


def test_delete_session():
    response = requests.delete(f'{main_route()}/sessions/1234').json()
    assert response.get('status') == 'OK'

def test_delete(delete_user):
    assert delete_user.get('status') == 'OK'