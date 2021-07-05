import pytest
import requests

def data():
    return {'token': '123123'}

@pytest.fixture
def get_main_route():
    from os import getenv
    main_route = getenv('MAKER_TEAMS_API_URL')
    return requests.get(main_route, data=data()).json()


def test_status(get_main_route):
    try:
        assert get_main_route.get('status') == 'OK'
    except:
        assert False


