from sqlalchemy.sql.functions import user
from routes import notifications
from flask import json, jsonify, request
from models.notification import Notification
from models.auth.authenticate_api_token import AuthAPI
from base64 import b64decode



def update_read_status(user_id):
    try:
        notifications = Notification.get_where('user_id', user_id)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })
    if not notifications:
        return jsonify({
            'status': 'error',
            'message': 'notification not found'
        }), 404
    try:
        for n in notifications:
            n.is_read = True
            n.save()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })
    return jsonify({
        'status': 'OK',
        'message': 'is_read updated'
    })

@notifications.route('/<user_id>', methods=['GET', 'PUT'], strict_slashes=False)
def get_by_user_id(user_id):
    """  """
    if request.method == 'PUT':
        return update_read_status(user_id)
    try: 
        results = Notification.get_where('user_id', user_id)
    except Exception as e:
        results = []

    if not results:
        return jsonify({
            'status': 'error',
            'message': 'No results'
        })
    try:
        results = list(map(lambda item: item.to_dict(), results))
        for item in results:
            b64_msg = item.get('msg')
            b64_bytes = b64_msg.encode('ascii')
            m_bytes = b64decode(b64_bytes)
            message = m_bytes.decode('ascii')
            item['msg'] = message
            del item['_sa_instance_state']
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e) + 'in here'
        })

    return jsonify({
        "status": "OK",
        "results": results
    })



@notifications.route('/<notification_id>', methods=['DELETE'], strict_slashes=False)
@AuthAPI.trusted_client
def index(notification_id):
    """  """
    try:
        notification = Notification.get_where("id", notification_id)
        if notification == []:
            notification = None        
    except Exception as e:
        print(f"Exception was raised {e}")
        notification = None

    if notification is None:
        raise Exception('Notification not found')
    notification[0].delete()
    # We need to respond to failed requests too
    return jsonify({"status": "OK", "message": "Notification Deleted"})


@notifications.route('/', methods=['POST'], strict_slashes=False)
@AuthAPI.trusted_client
def things():
    msg = request.args.get('msg') or request.form.get('msg')
    if not msg:
        return jsonify({
            'status': 'error',
            'message': 'Must include msg in your request'
        })
    user_id = request.args.get('user_id') or request.form.get('user_id')
    if not user_id:
        return jsonify({
            'status': 'error',
            'message': 'Must include user_id in your request'
        })
    if ' ' in msg:
        msg.replace(' ', '+')
    data = {
        'msg': msg.replace(' ', '+'),
        'user_id': user_id,
    }
    notification = Notification(**data)
    notification.save()

    return jsonify({
        "status": "OK",
        "data": f"{notification.to_dict()}"
    })