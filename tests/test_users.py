import pytest
import requests
from os import getenv


def data():
    return {'token': '123123'}

def main_route():
    return getenv('MAKER_TEAMS_API_URL')

@pytest.fixture
def get_all_users():
    return requests.get(f'{main_route()}/users', data=data()).json()

def test_get_all_users_status(get_all_users):
    assert get_all_users.get('status') == 'OK'

def dummy_user_info():
    return {
        'id': 1234,
        'login': 'fakehandle',
        'email': 'fake@email.com',
        'avatar_url': 'fakeavatarurl',
        'name': 'fakeuser',
        'access_token': 'fakeaccesstoken',
        'token': '123123'
        }


@pytest.fixture
def create_user():
    return requests.post(f'{main_route()}/users', data=dummy_user_info()).json()

def test_create_user_(create_user):
    assert create_user.get('status') == 'OK'
    user = create_user.get('user')
    assert int(user.get('id')) == dummy_user_info().get('id')

    

@pytest.fixture
def get_user_by_id():
    id = dummy_user_info().get('id')
    return requests.get(f'{main_route()}/users/{id}', data=data()).json()

def test_get_user_by_id_status(get_user_by_id):
    assert get_user_by_id.get('status') == 'OK'

@pytest.fixture
def get_user_by_handle():
    handle = dummy_user_info().get('login')
    return requests.get(f'{main_route()}/users/{handle}', data=data()).json()

def test_get_user_by_handle_status(get_user_by_handle):
    assert get_user_by_handle.get('status') == 'OK'

@pytest.fixture
def get_user_by_str_attribute():
    email = dummy_user_info().get('email')
    return requests.get(f'{main_route()}/users/email/{email}', data=data()).json()

def test_get_user_by_str_attribute_status(get_user_by_str_attribute):
    assert get_user_by_str_attribute.get('status') == 'OK'

@pytest.fixture
def get_user_by_int_attribute():
    return requests.get(f'{main_route()}/users/credits/100', data=data()).json()

def test_get_user_by_int_attribute_status(get_user_by_int_attribute):
    assert get_user_by_int_attribute.get('status') == 'OK'

@pytest.fixture
def update_user_attribute():
    id = dummy_user_info().get('id')
    updated_user = requests.put(f'{main_route()}/users/{id}/handle/some_test', data=data()).json()
    corrected_user = requests.put(f'{main_route()}/users/{id}/handle/fakeuser', data=data()).json()
    return updated_user, corrected_user

def test_update_user_attribute_status(update_user_attribute):
    for response in update_user_attribute:
        assert response.get('status') == 'OK'

@pytest.fixture
def delete_user():
    id = dummy_user_info().get('id')
    return requests.delete(f'{main_route()}/users/{id}', data=data()).json()

def test_delete_user_status(delete_user):
    assert delete_user.get('status') == 'OK'