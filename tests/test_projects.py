import pytest
import requests
from os import getenv


def data():
    return {'token': '123123'}

def main_route():
    return getenv('MAKER_TEAMS_API_URL')

def dummy_project_info():
    return {
        'token': 123123,
        'id': 123,
        'title': 'Historic Black Wallstreet Business Directory',
        'repository': 'hello-world',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipis',
        'preview_images': ['https://i.imgur.com/4Eso2sc.png', 'https://i.imgur.com/KR33ftT.png', 'https://i.imgur.com/tpGOXfD.png'],
        'videos': ['https://www.youtube.com/embed/hRFUZBXOWZI', 'https://www.youtube.com/embed/GAlKHqcnKTw'],
        'resources': [{'link':'https://www.azlyrics.com/n/nickelback.html', 'name': "The Meaning of Life"}],
        'quizzes': ['#THEREARENOQUIZESYET'],
        'goals': ['Put your left foot in', 'Your left foot out', 'Your left foot in',
                    'And shake it all about', 'You do the hokey pokey', 'And turn yourself around'],
        'dependencies': ['Python 3.8', 'Flask', 'The Will to Live'],
        'progress': '0',
        'sprints': ['Sprint 1', 'Sprint 2', 'Sprint 3']
    }

@pytest.fixture
def create_project():
    return requests.post(f'{main_route()}/projects', data=dummy_project_info()).json()

def test_create_project_(create_project):
    assert create_project.get('status') == 'OK'
    project = create_project.get('project')
    assert int(project.get('id')) == dummy_project_info().get('id')