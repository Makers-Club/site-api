from sqlalchemy.sql.expression import all_
from routes import events
from flask import json, jsonify, request
from models.events import Event
from models.auth.authenticate_api_token import AuthAPI

@events.route('/', methods=['POST', 'GET'], strict_slashes=False)
@AuthAPI.trusted_client
def get_or_create_events():
    from models.events import Event
    if request.method == 'POST':
        try:
            data = request.args or request.form
            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'must include creation data'
                })
            new_event = Event(**data)
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e) + 'TWO'
            })
        new_event.save()
        print('in HERE')
        new_event = new_event.to_dict()
        del new_event['_sa_instance_state']
        return jsonify({
            'status': 'OK',
            'message': 'event created',
            'event': new_event
        })
    try:
        all_events = Event.get_all()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e) + 'ONE'
        })
    if all_events:
        events = [event.to_dict() for event in all_events]
        for e in events:
            del e['_sa_instance_state']
    else:
        events = None
    return jsonify({
        'status': 'OK',
        'events': events
    })