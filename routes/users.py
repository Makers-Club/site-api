from routes import users
from flask import jsonify, request
from models.user import User
from models.auth.authenticate_api_token import AuthAPI

'''
The sub-functions here will be 'hidden' inside the User model after refactoring

prior to returning object.to_dict() for anything,
we must do -> del object._sa_instance_state 
to avoid the following error.
TypeError: Object of type InstanceState is not JSON serializabley default
We can't just remove this in the base model because that would prevent us
from being able to commit changes to the DB.
'''


# GET -------------------

def remove_private_user_data(user, users=None):
    if not users:
        del user['access_token']
        del user['credits']
        del user['email']
        del user['id']
        return user
    for user in users:
        del user['access_token']
        del user['credits']
        del user['email']
        del user['id']
    return users


@users.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all():
    if request.method == 'POST':
        if not request.permission == 'admin':
            return jsonify({
            'status': 'error',
            'message': 'You do not have permission to perform that action.',
            'users': None
            }), 500
        print('IN POST')
        return create_new_user(request)
    users = User.get_all_list_of_dicts()
    if not users:
        return jsonify({
            'status': 'error',
            'users': None
            }), 500
    if request.permission != 'admin':
        users = remove_private_user_data(1, users)
    return {
        'status': 'OK',
        'users': users
        }

@users.route('/<id>', methods=['DELETE'], strict_slashes=False)
@users.route('/<int:id>', methods=['GET'], strict_slashes=False)
@users.route('/<handle>', methods=['GET'], strict_slashes=False)
@AuthAPI.trusted_client
def by_id(id=None, handle=None):
    if handle:
        return get_by_handle(handle)
    user = User.get_by_id(id)
    if not user:
        return jsonify({
            'status': 'error',
            'user': None
        }), 404
    if request.method == 'DELETE':
        if not request.client.client_id == id and not request.permission == 'admin':
            return jsonify({
                'status': 'error',
                'message': 'You do not have permission to perform this action.',
                'user': None
            })
        from models.auth.token import Token
        if not request.permission == 'admin':
            request.client.delete()
        else:
            users_token = Token.get_where('client_id', id)
            if users_token:
                users_token[0].delete()
        return delete_user(user)
    try:
        print('1')
        del user._sa_instance_state
    except:
        pass
    if not str(id) == request.client.client_id and not request.permission == 'admin':
        user = remove_private_user_data(user.to_dict())
    else:
        user = user.to_dict()
    return jsonify({
        'status': 'OK',
        'user': user
    }), 200

def get_by_handle(handle):
    user = User.get_by_handle(handle)
    if not user:
        return jsonify({
            'status': 'error',
            'user': None
        }), 404
    try:
        print('2')
        del user._sa_instance_state
    except:
        pass
    from models.auth.token import Token
    client_id = request.client.client_id
    if client_id != user.id:
        user = remove_private_user_data(user.to_dict())
    else:
        user = user.to_dict()
    return jsonify({
        'status': 'OK',
        'user': user
    }), 200


@users.route('/<attribute>/<value>/', methods=['GET'], strict_slashes=False)
@AuthAPI.trusted_client
def by_attribute(attribute, value, new_value=None):
    if value != 'access_token' and isinstance(value, str):
        value = str(value).lower()
    users = User.get_where(attribute.lower(), value)
    if not users:
            return jsonify({
                'status': 'error',
                'user': None
            }), 404
    user_dicts = []
    for user in users:
        try:
            print('3')
            del user._sa_instance_state
        except:
            pass
        user_dicts.append(user.to_dict())
    if not request.permission == 'admin':
        user_dicts = remove_private_user_data(1, user_dicts)
    return jsonify({
        'status': 'OK',
        'users': user_dicts
    }), 200
    

# UPDATE -------------------

def sql_injection(attribute, value):
    # use regex to check for sql injection?
    # just creating this, which does nothing now, so we don't forget
    return False

@users.route('/<id>', methods=['PUT'], strict_slashes=False)
@AuthAPI.trusted_client
def update(id):
    if not request.client.client_id == id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to perform this action.',
            'user': None
        })
    user = User.get_by_id(id)
    if not user:
         return jsonify({
            'status': 'error',
            'user': None
        })
    user.update(attrs=request.form)
    return jsonify({
        'status': 'OK',
        'user': user.to_dict()
    })       
@users.route('/<id>/<attribute>/<value>', methods=['PUT'], strict_slashes=False)
@AuthAPI.trusted_client
def update_attr(id, attribute, value):
    if not request.client.client_id == id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to perform this action.',
            'user': None
        })
    user = User.get_by_id(id)
    if not user or sql_injection(attribute, value):
        return jsonify({
            'status': 'error',
            'user': None
        })
    user.update_attr(attribute, value)
    """        
    # updating an object with obj.__dict__[attribute] = value was not working for me at all
    # I had to resort to saving a dictionary of the obj, deleting it from the db, then recreating it
    user_dict = user.to_dict()
    user.delete()
    # this line below ensures we save the updated value as the correct data type
    # type(user.__dict__[attribute]) evaluates to the type itself, so next to (value) it is just typecasting
    # just like if you hard-code int('33') or something like that
    user_dict[attribute] = type(user.__dict__[attribute])(value)
    user = User(**user_dict)
    """
    user.save()
    try:
        print('4')
        del user._sa_instance_state
    except:
        pass
    return jsonify({
        'status': 'OK',
        'user': user.to_dict()
    })

# CREATE -------------------

def create_new_user(request):
    if not 'id' in request.form and not 'id' in request.args:
        return jsonify({
            'status': 'error',
            'message': 'new user data was bad'
        }), 400
    if request.form:
        new_user = User(**request.form)
    else:
        new_user = User(*request.args)
    if not new_user:
        return jsonify({
            'status': 'error',
            'message': 'new user data was bad'
        }), 400
    new_user.save()
    print('saved new user')
    from models.events import Event
    data = {
        'user_handle': new_user.handle,
        'user_pic': new_user.avatar_url,
        'type': 'NEW_USER'
    }
    new_event = Event(**data)
    new_event.save()
    try:
        print('5')
        del new_user._sa_instance_state
    except:
        pass
    from models.auth.token import Token
    new_token = Token(new_user.id, new_user.access_token)
    new_token.save()
    try:
        print('6')
        del new_token._sa_instance_state
    except:
        pass
    return jsonify({
        'status': 'OK',
        'user': new_user.to_dict()
    }), 200




# DELETE -------------------

def delete_user(user):
    id = user.id
    user.delete()
    return jsonify({
        'status': 'OK',
        'user': f'{id} deleted'
        })