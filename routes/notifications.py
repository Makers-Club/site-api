from routes import notifications
from flask import jsonify, request
from models.notification import Notification
from models.auth.authenticate_api_token import AuthAPI
from base64 import b64decode

@notifications.route('/<user_id>', methods=['GET'], strict_slashes=False)
def get_by_user_id(user_id):
    """  """
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