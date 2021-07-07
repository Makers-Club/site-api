from models.projects import Project
from routes import projects
from flask import request, jsonify
from models.auth.authenticate_api_token import AuthAPI

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
        print(request.form, 'FORM IN HERE')
        new_project = Project(**request.form)
    else:
        print(request.form, 'ARGS IN HERE')
        new_project = Project(*request.args)
    if not new_project:
        return jsonify({
            'status': 'error',
            'message': 'new project data was bad'
        }), 400
    print(new_project.to_dict(), '*****\n\n\n')
    new_project.save()
    del new_project._sa_instance_state
    return jsonify({
        'status': 'OK',
        'project': new_project.to_dict()
    }), 200