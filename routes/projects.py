from models.projects import Project
from routes import projects
from flask import request, jsonify
from models.auth.authenticate_api_token import AuthAPI

@projects.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all():
    if request.method == 'POST':
        return create_new_obj(Project, 'project', request)
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


def create_new_obj(cls_name, cls_name_str, request):
    if request.form:
        new_obj = cls_name(**request.form)
    else:
        new_obj = cls_name(*request.args)
    if not new_obj:
        return jsonify({
            'status': 'error',
            'message': f'new {cls_name_str} data was bad'
        }), 400
    new_obj.save()
    del new_obj._sa_instance_state
    return jsonify({
        'status': 'OK',
        f'{cls_name_str}': new_obj.to_dict()
    }), 200


@projects.route('/<int:id>', methods=['GET'], strict_slashes=False)
@AuthAPI.trusted_client
def by_id(id=None, handle=None):
    project = Project.get_by_id(id)
    if not project:
        return jsonify({
            'status': 'error',
            'project': None
        }), 404
    del project._sa_instance_state
    return jsonify({
            'status': 'OK',
        'project': project.to_dict()
    }), 200





# HACKING IT YOOOOOOO

from routes import learning_resources, project_templates, sprint_templates, sprints, task_templates, tasks
from models.projects import LearningResource, Project, ProjectTemplate, Sprint, SprintTemplate, Task, TaskTemplate

@learning_resources.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all_learning_resources():
    if request.method == 'POST':
        return create_new_obj(LearningResource, 'learning_resource', request)
    learning_resources = LearningResource.get_all_list_of_dicts()
    if not learning_resources:
        return jsonify({
            'status': 'error',
            'learning_resources': None
            }), 500
    return {
        'status': 'OK',
        'learning_resources': learning_resources
        }

@project_templates.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all_project_templates():
    if request.method == 'POST':
        return create_new_obj(ProjectTemplate, 'project_template', request)
    project_templates = ProjectTemplate.get_all_list_of_dicts()
    if not project_templates:
        return jsonify({
            'status': 'error',
            'project_templates': None
            }), 500
    return {
        'status': 'OK',
        'project_templates': project_templates
        }

@sprint_templates.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all_sprint_templates():
    if request.method == 'POST':
        return create_new_obj(SprintTemplate, 'sprint_template', request)
    sprint_templates = SprintTemplate.get_all_list_of_dicts()
    if not sprint_templates:
        return jsonify({
            'status': 'error',
            'sprint_templates': None
            }), 500
    return {
        'status': 'OK',
        'sprint_templates': sprint_templates
        }

@sprints.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all_sprints():
    if request.method == 'POST':
        return create_new_obj(Sprint, 'sprint', request)
    sprints = Sprint.get_all_list_of_dicts()
    if not sprints:
        return jsonify({
            'status': 'error',
            'sprints': None
            }), 500
    return {
        'status': 'OK',
        'sprints': sprints
        }



@task_templates.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all_task_templates():
    if request.method == 'POST':
        return create_new_obj(TaskTemplate, 'task_template', request)
    task_templates = TaskTemplate.get_all_list_of_dicts()
    if not task_templates:
        return jsonify({
            'status': 'error',
            'task_templates': None
            }), 500
    return {
        'status': 'OK',
        'task_templates': task_templates
        }

@tasks.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all_tasks():
    if request.method == 'POST':
        return create_new_obj(Task, 'task', request)
    tasks = Task.get_all_list_of_dicts()
    if not tasks:
        return jsonify({
            'status': 'error',
            'tasks': None
            }), 500
    return {
        'status': 'OK',
        'tasks': tasks
        }