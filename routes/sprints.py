from models.sprint import Sprint
from routes import sprints
from flask import json, request, jsonify
from models.auth.authenticate_api_token import AuthAPI
from models.events import Event
from models.projects import Project



@sprints.route('/', methods=['POST', 'GET'], strict_slashes=False)
def create_sprint():
    # THIS WILL ONLY BE POST SOON
    if request.method == 'GET':
        sprints = Sprint.get_all()
        if sprints:
            sprints = [s.to_dict() for s in sprints]
            for s in sprints:
                del s['_sa_instance_state']
        return jsonify({
            'status': 'OK',
            'sprints': sprints
        })
    if request.form:
        sprint = Sprint(**request.form)
    else:
        sprint = Sprint(**request.args)
    if not sprint:
        return jsonify({
            'status': 'error',
            'message': f'new sprint data was bad'
        }), 400
    sprint.save()
    sprint_dict = sprint.to_dict()
    print('\n\tSPRINT TO_DICT\n\t', sprint_dict, '\n')
    sprint_project = Project.get_by_id(sprint.project_id)
    print('SPRINT PROJECT:\n\t', sprint_project)
    from models.user import User
    project_owner = User.get_by_handle(sprint_project.owner_handle)
    if not project_owner:
        return jsonify({
            'status': 'error',
            'message': f'project owner not found'
        }), 400
    avatar_url = project_owner.avatar_url
    event_data = {
        'user_handle': sprint_project.owner_handle,
        'user_link': '127.0.0.1:8080/users/' + sprint_project.owner_handle,
        'project_name': sprint_project.name,
        'project_link': f'/projects/{sprint_project.id}',
        'sprint_link': f'/sprints/{sprint.id}',
        'sprint_number': f'{sprint.id}',
        'type': 'SPRINT_STARTED',
        'user_pic': avatar_url
    }
    sprint_creation_event = Event(**event_data)
    sprint_creation_event.save()
    try:
        del sprint_dict['_sa_instance_state']
    except:
        pass
    return jsonify({
        'status': 'OK',
        f'sprint': sprint_dict
    }), 200


@sprints.route('/<id>', methods=['PUT'], strict_slashes=False)
def update_sprint(id):
    sprint = Sprint.get_by_id(id)
    if not sprint:
        return jsonify({
            'status': 'error',
            'message': 'Sprint not found'
        }), 404
    data = request.form or request.args
    try:
        sprint.update(**data)
        sprint.save()
        sprint_dict = sprint.to_dict()
        print('\n\tSPRINT TO_DICT\n\t', sprint_dict, '\n')
        sprint_project = Project.get_by_id(sprint.project_id)
        print('SPRINT PROJECT:\n\t', sprint_project)
        from models.user import User
        project_owner = User.get_by_handle(sprint_project.owner_handle)
        if not project_owner:
            return jsonify({
                'status': 'error',
                'message': f'project owner not found'
            }), 400
        avatar_url = project_owner.avatar_url
        event_data = {
            'user_handle': sprint_project.owner_handle,
            'user_link': '127.0.0.1:8080/users/' + sprint_project.owner_handle,
            'project_name': sprint_project.name,
            'project_link': f'/projects/{sprint_project.id}',
            'sprint_link': f'/sprints/{sprint.id}',
            'sprint_number': f'{sprint.id}',
            'type': 'SPRINT_COMPLETED',
            'user_pic': avatar_url
        }
        sprint_creation_event = Event(**event_data)
        sprint_creation_event.save()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })
    try:
        del sprint._sa_instance_state
    except:
        pass
    sprint_dict = sprint.to_dict()
    return jsonify({
        'status': 'OK',
        'sprint': sprint_dict
    })