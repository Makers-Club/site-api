from functools import wraps
from flask import request, jsonify


class AuthAPI():
    @staticmethod
    def trusted_client(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'client') or not request.client:
                return jsonify({
                    'status': 'error',
                    'message': 'bad or missing API token'
                    })
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def admin_only(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'permission') or not request.permission == 'admin':
                return jsonify({
                    'status': 'error',
                    'message': 'you do not have permission to do this'
                    })
            return f(*args, **kwargs)
        return decorated_function
    
    @classmethod
    def trusted(cls, request):
        from models.auth.token import Token
        id = request.form.get('token')
        if not id:
            id = request.args.get('token')
            if not id:
                return None
        client = Token.get_by_id(id)
        if client:
            permission = client.permission
        else:
            permission = None
        return client, permission
