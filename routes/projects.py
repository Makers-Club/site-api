from models.projects import Project
from routes import projects
from flask import request, jsonify
from models.auth.authenticate_api_token import AuthAPI
from models.events import Event

@projects.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all():
    if request.method == 'POST':
        return create_new_project(request)
    projects = Project.get_all_list_of_dicts()
    if not projects:
        return jsonify({
            'status': 'error',
            'projects': None
            }), 500
    return {
        'status': 'OK',
        'projects': projects
        }


def create_new_project(request):
    if request.form:
        project = Project(**request.form)
    else:
        project = Project(**request.args)
    if not project:
        return jsonify({
            'status': 'error',
            'message': f'new project data was bad'
        }), 400
    project.save()
    project_dict = project.to_dict()
    from models.user import User
    project_owner = User.get_by_handle(project.owner_handle)
    if not project_owner:
        return jsonify({
            'status': 'error',
            'message': f'project owner not found'
        }), 400
    avatar_url = project_owner.avatar_url
    event_data = {
        'user_handle': project.owner_handle,
        'user_link': '127.0.0.1:8080/users/' + project.owner_handle,
        'project_name': project.name,
        'project_link': f'/projects/{project.id}',
        'type': 'PROJECT_STARTED',
        'user_pic': avatar_url
    }
    print(event_data)
    project_creation_event = Event(**event_data)
    project_creation_event.save()
    del project_dict['_sa_instance_state']
    return jsonify({
        'status': 'OK',
        f'project': project_dict
    }), 200




@projects.route('/<id>', methods=['GET'], strict_slashes=False)
@AuthAPI.trusted_client
def by_id(id=None, handle=None):
    project = Project.get_by_id(id)
    if not project:
        return jsonify({
            'status': 'error',
            'project': None
        }), 404
    project_dict = project.to_dict()
    del project_dict['_sa_instance_state']
    return jsonify({
            'status': 'OK',
        'project': project_dict
    }), 200

