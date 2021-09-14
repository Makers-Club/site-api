from models.sprint import Sprint
from routes import sprints
from flask import json, request, jsonify
from models.auth.authenticate_api_token import AuthAPI
from models.events import Event



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
    from models.projects import Project
    if request.form:
        print('*****', request.form, '\n\n')
        sprint = Sprint(**request.form)
    else:
        print('*****', request.args, '\n\n')
        sprint = Sprint(**request.args)
    if not sprint:
        return jsonify({
            'status': 'error',
            'message': f'new sprint data was bad'
        }), 400
    sprint.save()
    sprint_dict = sprint.to_dict()
    print(sprint.to_dict())
    sprint_project = Project.get_by_id(sprint.project_id)
    event_data = {
        'user_handle': sprint_project.owner_handle,
        'user_link': '127.0.0.1:8080/users/' + sprint_project.owner_handle,
        'project_name': sprint_project.name,
        'project_link': f'/projects/{sprint_project.id}',
        'sprint_link': f'/sprints/{sprint.id}',
        'type': 'SPRINT_STARTED'
    }
    print(event_data)
    sprint_creation_event = Event(**event_data)
    sprint_creation_event.save()
    del sprint_dict['_sa_instance_state']
    return jsonify({
        'status': 'OK',
        f'sprint': sprint_dict
    }), 200