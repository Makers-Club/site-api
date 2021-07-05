from routes import sessions
from flask import jsonify, request
from models.auth.session import Session





@sessions.route('/', methods=['GET'], strict_slashes=False)
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
    del session._sa_instance_state
    return jsonify({
        'status': 'OK',
        'session': session.to_dict()
    })

@sessions.route('/<cookie>', methods=['GET'], strict_slashes=False)
@sessions.route('/<user_id>', methods=['DELETE'], strict_slashes=False)
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
        del user._sa_instance_state
        return jsonify({
            'status': 'OK',
            'user': user.to_dict()
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