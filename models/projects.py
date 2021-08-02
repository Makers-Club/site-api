from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4

def to_many(child_class_name, this_table_name):
    return relationship(child_class_name, backref=this_table_name)

def to_one(parent_dot_id_str, data_type, len=None):
    return Column(data_type(len), ForeignKey(parent_dot_id_str))

'''users_and_projects = Table('association', declarative_base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('project_id', ForeignKey('projects.id'), primary_key=True)
)'''
from models.user import users_and_projects

class LearningResource(Base, declarative_base):
    __tablename__ = 'learn_resources'
    # PARENTS ------------------------------------------------
    # which type of project this belongs to String(128), ForeignKey('project_templates.id')
    project_template_id = to_one('project_templates.id', String, 128)
    # which type of sprint this belongs to
    sprint_template_id = to_one('sprint_templates.id', String, 128)
    # which type of task this belongs to
    task_template_id = to_one('task_templates.id', String, 128)
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    articles = Column(String(128))
    videos = Column(String(128))
    external_links = Column(String(128))
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.articles = kwargs.get('articles')
            self.videos = kwargs.get('videos')
            self.external_links = kwargs.get('external_links')



class ProjectTemplate(Base, declarative_base):
    __tablename__ = 'project_templates'
    # CHILDREN -----------------------------------------------
    # so we can find all of a given type of project users made
    projects = to_many("Project", "project_templates")
    # so we know what sprint types are associated with this project type
    sprint_templates = to_many("SprintTemplate", "project_templates")
    # learning resources for this at the project level
    learning_resources = to_many("LearningResource", "project_templates")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    name = Column(String(128))
    link = Column(String(128))
    author = Column(String(128))
    tech_dependencies = Column(String(128))
    role_types = Column(String(128))
    description = Column(String(256))
    goals = Column(String(128))
    quiz = Column(String(128))
    preview_images = Column(String(128))
    cost = Column(Integer)
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.name = kwargs.get('name')
            self.link = kwargs.get('link')
            self.author = kwargs.get('author')
            self.tech_dependencies = kwargs.get('tech_dependencies')
            self.role_types = kwargs.get('role_types') # list of titles?
            self.description = kwargs.get('description')
            self.goals = kwargs.get('goals')
            self.quiz = kwargs.get('quiz') # quiz table
            self.preview_images = kwargs.get('preview_images')
            self.cost = 5
            


class Project(Base, declarative_base):
    __tablename__ = 'projects'
    # PARENTS ------------------------------------------------
    # which type of project this is
    project_template_id = to_one('project_templates.id', String, 128) 
    # CHILDREN -----------------------------------------------
    # the actual sprints the user works on in this project
    sprints = to_many("Sprint", "projects")
    # MANY TO MANY
    my_users = relationship(
        "User",
        secondary=users_and_projects,
        back_populates="my_projects")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=True)
    repository_link = Column(String(128), nullable=True)
    progress = Column(String(128))
    quiz_status = Column(String(128))
    roles = Column(String(128), nullable=True)   
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = str(uuid4())
            self.name = kwargs.get('name')
            self.repository_link = kwargs.get('repository_link')
            self.progress = kwargs.get('progress')
            self.quiz_status = kwargs.get('quiz_status')
            self.roles = kwargs.get('roles')
            

class SprintTemplate(Base, declarative_base):
    __tablename__ = 'sprint_templates'
    # PARENTS ------------------------------------------------
    # which type of project this is in
    project_template_id = to_one('project_templates.id', String, 128) 
    # CHILDREN -----------------------------------------------
    # which actual sprints of this type are being worked on by users
    sprints = to_many("Sprint", "sprint_templates")
    # which type of tasks this has in it
    task_templates = to_many("TaskTemplate", "sprint_templates")
    # learning resources for this at the sprint level
    learning_resources = to_many("LearningResource", "sprint_templates")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    number = Column(Integer)
    tech_dependencies = Column(String(128))
    role_types = Column(String(128))
    description = Column(String(256))
    goals = Column(String(128))
    quiz = Column(String(128))
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.number = kwargs.get('number')
            self.tech_dependencies = kwargs.get('tech_dependencies')
            self.role_types = kwargs.get('role_types') # list of titles?
            self.description = kwargs.get('description')
            self.goals = kwargs.get('goals')
            self.quiz = kwargs.get('quiz') # quiz table

class Sprint(Base, declarative_base):
    __tablename__ = 'sprints'
    # PARENTS ------------------------------------------------
    # which type of sprint this is in
    sprint_template_id = to_one('sprint_templates.id', String, 128)
    # which actual project this is part of
    project_id = to_one('projects.id', String, 128) 
    # CHILDREN -----------------------------------------------
    # which actual tasks it has in it
    tasks = to_many("Task", "sprints")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    progress = Column(String(128))
    quiz_status = Column(String(128))
    roles = Column(String(128))   
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.progress = kwargs.get('progress')
            self.quiz_status = kwargs.get('quiz_status')
            self.roles = kwargs.get('roles')


class TaskTemplate(Base, declarative_base):
    __tablename__ = 'task_templates'
    # PARENTS ------------------------------------------------
    # which type of sprint this is in
    sprint_template_id = to_one('sprint_templates.id', String, 128)
    # CHILDREN -----------------------------------------------
    # which actual tasks it has in it
    tasks = to_many("Task", "task_templates")
    # learning resources for this at the task level
    learning_resources = to_many("LearningResource", "task_templates")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    number = Column(Integer)
    tech_dependencies = Column(String(128))
    role_types = Column(String(128))
    description = Column(String(256))
    goals = Column(String(128))
    tests = Column(String(128))
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.number = kwargs.get('number')
            self.tech_dependencies = kwargs.get('tech_dependencies')
            self.role_types = kwargs.get('role_types') # list of titles?
            self.description = kwargs.get('description')
            self.goals = kwargs.get('goals')
            self.tests = kwargs.get('tests') # quiz table

class Task(Base, declarative_base):
    __tablename__ = 'tasks'
    # PARENTS ------------------------------------------------
    # which type of task this is
    task_template_id = to_one('task_templates.id', String, 128)
    # which actual sprint this is in
    sprint_id = to_one('sprints.id', String, 128)
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    status = Column(String(128))   
    role = Column(String(128))  
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.status = kwargs.get('status')
            self.role = kwargs.get('role')



