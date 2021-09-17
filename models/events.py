
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.sql.expression import null
from models.base import declarative_base, Base
from uuid import uuid4


class Event(Base, declarative_base):
    __tablename__ = 'events'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    message = Column(String(512), nullable=False)
    user_handle = Column(String(128), nullable=True)
    user_link = Column(String(128), nullable=True)
    sprint_number = Column(String(128), nullable=True)
    sprint_link = Column(String(128), nullable=True)
    project_name = Column(String(128), nullable=True)
    project_link = Column(String(128), nullable=True)
    type = Column(String(128), nullable=True)
    user_pic = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__()
        del self.id
        self.user_handle = kwargs.get('user_handle')
        self.user_link = kwargs.get('user_link')
        self.sprint_number = kwargs.get('sprint_number')
        self.sprint_link = kwargs.get('sprint_link')
        self.project_name = kwargs.get('project_name')
        self.project_link = kwargs.get('project_link')
        self.user_pic = kwargs.get('user_pic')
        self.type = kwargs.get('type')
        self.message = self.build_message(kwargs)

    @staticmethod
    def build_message(kwargs):
        msg_type = kwargs.get('type')
        if msg_type == 'PROJECT_STARTED':
            user_handle = kwargs.get('user_handle')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            user_pic = kwargs.get('user_pic')
            return f'<a class="event_user_handle" href="/users/{user_handle}"> <img class="mr-3 profile_pic" height="22" width="22" src="{user_pic}"> {user_handle}</a> created a new project, <a class="event_project_name" href="{project_link}">{project_name}</a>'
        if msg_type == 'SPRINT_STARTED':
            user_handle = kwargs.get('user_handle')
            user_link = kwargs.get('user_link')
            sprint_number = kwargs.get('sprint_number')
            sprint_link = kwargs.get('sprint_link')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            user_pic = kwargs.get('user_pic')
            return f'<a class="event_user_handle" href="/users/{user_handle}"> <img class="mr-3 profile_pic" height="22" width="22" src="{user_pic}"> {user_handle}</a> started <a class="event_sprint_number" href="{sprint_link}">Sprint {sprint_number}</a> of <a class="event_project_name" href="{project_link}">{project_name}</a>'
        if msg_type == 'SPRINT_COMPLETED':
            user_handle = kwargs.get('user_handle')
            user_link = kwargs.get('user_link')
            sprint_number = kwargs.get('sprint_number')
            sprint_link = kwargs.get('sprint_link')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            user_pic = kwargs.get('user_pic')
            return f'<a class="event_user_handle" href="/users/{user_handle}"> <img class="mr-3 profile_pic" height="22" width="22" src="{user_pic}"> {user_handle}</a> completed <a class="event_sprint_number" href="{sprint_link}">Sprint {sprint_number}</a> of <a class="event_project_name" href="{project_link}">{project_name}</a>'
        if msg_type == 'NEW_USER':
            user_handle = kwargs.get('user_handle')
            user_pic = kwargs.get('user_pic')
            return f'<a class="event_user_handle" href="/users/{user_handle}"> <img class="mr-3 profile_pic" height="22" width="22" src="{user_pic}"> {user_handle}</a> joined Maker Teams! Welcome them on slack! <a class="s_tiny" target="_blank" href="https://join.slack.com/t/makerteams/shared_invite/zt-vrynuzza-goE5OE4xrulkceQE0Mt3Hw"><img src="https://cdn.brandfolder.io/5H442O3W/at/pl546j-7le8zk-6gwiyo/Slack_Mark.svg"/></a>'
        if msg_type == 'JOINED_SPRINT':
            # perm link if above stops working https://join.slack.com/t/makerteams/shared_invite/zt-w1cjhnup-BxQz1UzKYvaN9Nn8AeHqNA
            user_handle = kwargs.get('user_handle')
            user_link = kwargs.get('user_link')
            sprint_number = kwargs.get('sprint_number')
            sprint_link = kwargs.get('sprint_link')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            user_pic = kwargs.get('user_pic')
            return f'<a class="event_user_handle" href="/users/{user_handle}"> <img class="mr-3 profile_pic" height="22" width="22" src="{user_pic}"> {user_handle}</a> joined <a class="event_sprint_number" href="{sprint_link}">Sprint {sprint_number}</a> of <a class="event_project_name" href="{project_link}">{project_name}</a>'
        if msg_type == 'GAVE_PROJECT_FEEDBACK':
            user_handle = kwargs.get('user_handle')
            user_link = kwargs.get('user_link')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            user_pic = kwargs.get('user_pic')
            return f'<a class="event_user_handle" href="/users/{user_handle}"> <img class="mr-3 profile_pic" height="22" width="22" src="{user_pic}"> {user_handle}</a> gave feedback on <a class="event_project_name" href="{project_link}">{project_name}</a>'

