from models.projects import Project
from routes import projects
from flask import request, jsonify
from models.auth.authenticate_api_token import AuthAPI
from copy import copy

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
        project = Project(*request.args)
    if not project:
        return jsonify({
            'status': 'error',
            'message': f'new project data was bad'
        }), 400
    template_id = request.args.get('project_template_id') or '4cca0b4b-e745-40e2-b1dd-ee3e8e6ec577'
    # associate project and template with one another
    project.project_template_id = template_id
    project_template = ProjectTemplate.get_by_id(template_id)
    project_template.projects.append(project)
    # for each type of sprint in this project template
    # create an actual sprint, associate it with the actual project
    sprints = []
    for sprint_template in project_template.sprint_templates:
        sprint = Sprint()
        sprint.project_id = project.id
        # associate it with its template
        sprint.sprint_template_id = sprint_template.id
        tasks = []
        # for each type of task in each sprint template
        for task_template in sprint_template.task_templates:
            # create an actual task and associate it with its template
            task = Task()
            task.task_template_id = task_template.id
            # associate it with its actual sprint
            task.sprint_id = sprint.id
            # associate its template with it (reverse of above)
            task_template.tasks.append(task)
            # add to list of tasks to be added to sprint after
            tasks.append(task)
            task.save()
        sprint.tasks = tasks
        sprint.save()
        # add to a list of sprints, to be connected to actual project after
        sprints.append(sprint)
    project.sprints = sprints
    project.save()
    project_dict = copy_project_into_dict(project)
    return jsonify({
        'status': 'OK',
        f'project': project_dict
    }), 200

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
    obj_dict = {}
    for k, v in new_obj.__dict__.items():
        if hasattr(v, 'id'):
            obj_dict[k] = v.id
            continue
        if isinstance(v, list):
            obj_dict[k] = [x.id for x in v]
            continue
        if k != '_sa_instance_state':
            obj_dict[k] = v
    return jsonify({
        'status': 'OK',
        f'{cls_name_str}': obj_dict
    }), 200


def copy_project_into_dict(project):
    new = {
        'project_template_id': project.project_template_id,
        'id': project.id,
        'name': project.name,
        'repository_link': project.repository_link,
        'progress': project.progress,
        'quiz_status': project.quiz_status,
        'roles': project.roles
    }
    return new


@projects.route('/<id>', methods=['GET'], strict_slashes=False)
@AuthAPI.trusted_client
def by_id(id=None, handle=None):
    project = Project.get_by_id(id)
    if not project:
        return jsonify({
            'status': 'error',
            'project': None
        }), 404
    project_dict = copy_project_into_dict(project)
    project_dict['sprints'] = [s.id for s in project.sprints]
    return jsonify({
            'status': 'OK',
        'project': project_dict
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