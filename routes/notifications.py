from routes import notifications
from flask import jsonify, request
from models.notification import Notification
from models.auth.authenticate_api_token import AuthAPI

@notifications.route('/<user_id>', methods=['GET'], strict_slashes=False)
def get_by_user_id(user_id):
    """  """
    try: 
        results = Notification.get_where('user_id', user_id)
    except:
        results = []

    results = list(map(lambda item: item.to_dict(), results))
    for item in results:
        del item['_sa_instance_state']

    return jsonify({
        "status": "OK",
        "results": results
    })


@notifications.route('/<notification_id>', methods=['POST', 'DELETE'], strict_slashes=False)
@AuthAPI.trusted_client
def index(notification_id):
    """  """
    try:
        notification = Notification.get_where("id", notification_id)
    except Exception as e:
        print(f"Exception was raised {e}")
        notification = None

    query_string = request.query_string.decode('utf-8')
    data = {}
    for item in query_string.split('&'):
        key, value = item.split('=')
        if key == 'token':
            continue
        data[key] = value.replace('-', ' ')
    data['is_read'] = False

    if request.method == "POST":
        if notification is not None:
            raise Exception('Notification already exists')
        notification = Notification(**data)
        notification.save()

        return jsonify({
            "status": "OK",
            "data": f"{notification.to_dict()}"
        })

    if request.method == "DELETE":
        if notification is None:
            raise Exception('Notification not found')
        notification[0].delete()
        return jsonify({"status": "OK", "message": "Notification Deleted"})
    
    return jsonify({
        "status": "OK",
        "query_string": f"{data}"
    })
