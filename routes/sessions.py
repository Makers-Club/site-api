from routes import sessions
from flask import jsonify, request
from models.auth.session import Session
from models.auth.authenticate_api_token import AuthAPI



@sessions.route('/', methods=['GET'], strict_slashes=False)
@AuthAPI.trusted_client
def get_all_sessions():
    sessions = Session.get_all_list_of_dicts()
    if not sessions:
        return jsonify({
            'status': 'error',
            'sessions': None
            }), 500
    return {
        'status': 'OK',
        'sessions': sessions
        }

@sessions.route('/<token>/<user_id>', methods=['POST'], strict_slashes=False)
@AuthAPI.trusted_client
def create_session(token, user_id):
    from models.user import User
    # check if user id is real
    user = User.get_by_id(user_id)
    if user:
        # if session already exists, update timestamp
        session = Session.get_by_id(token)
        if session:
            from datetime import datetime
            session.created_at = datetime.now()
        else:
            session = Session(token=token, user_id=user_id)
    if not user or not session:
        return jsonify({
            'status': 'error',
            'session': None
        })
    session.save()
    session_dict = {
        'created_at': str(session.created_at),
        'user_id': session.user_id,
        'id': session.id
    }
    return jsonify({
        'status': 'OK',
        'session': session_dict
    })

@sessions.route('/<cookie>', methods=['GET'], strict_slashes=False)
@sessions.route('/<user_id>', methods=['DELETE'], strict_slashes=False)
@AuthAPI.trusted_client
def check_or_delete_session(cookie=None, user_id=None):
    if request.method == 'GET':
        user_id = Session.user_by_session(cookie)
        if not user_id:
            return jsonify({
                'status': 'error',
                'user': None
            })
        from models.user import User
        user = User.get_by_id(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'user': None
            })
        user_dict = {
            'id': user.id,
            'email': user.email,
            'credits': user.credits,
            'name': user.name,
            'handle': user.handle,
            'avatar_url': user.avatar_url,
            'access_token': user.access_token,
            'projects': user.my_projects
        }
        return jsonify({
            'status': 'OK',
            'user': user_dict
        })
    if request.method == 'DELETE':
        sessions = Session.sessions_by_user(user_id)
        if not sessions:
            return jsonify({
                'status': 'error',
                'session': None
                })
        for session in sessions:
            session.delete()
        return jsonify({
            'status': 'OK'
        })
