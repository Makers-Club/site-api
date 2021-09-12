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
    except:
        results = []

    results = list(map(lambda item: item.to_dict(), results))
    for item in results:
        b64_msg = item['msg']
        b64_bytes = b64_msg.encode('ascii')
        m_bytes = b64decode(b64_bytes)
        message = m_bytes.decode('ascii')
        item['msg'] = message
        del item['_sa_instance_state']

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
    data = request.args.to_dict()

    data['msg'] = data['msg'].replace(' ', '+')
    data['is_read'] = True if data['is_read'] == 'true' else False

    notification = Notification(**data)
    notification.save()

    return jsonify({
        "status": "OK",
        "data": f"{notification.to_dict()}"
    })