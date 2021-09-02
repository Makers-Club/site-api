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



@users.route('/', methods=['GET', 'POST'], strict_slashes=False)
@AuthAPI.trusted_client
def all():
    if request.method == 'POST':
        return create_new_user(request)
    users = User.get_all_list_of_dicts()
    if not users:
        return jsonify({
            'status': 'error',
            'users': None
            }), 500
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
        return delete_user(user)
    del user._sa_instance_state
    return jsonify({
            'status': 'OK',
        'user': user.to_dict()
    }), 200

def get_by_handle(handle):
    user = User.get_by_handle(handle)
    if not user:
        return jsonify({
            'status': 'error',
            'user': None
        }), 404
    del user._sa_instance_state
    return jsonify({
        'status': 'OK',
        'user': user.to_dict()
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
        del user._sa_instance_state
        user_dicts.append(user.to_dict())
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
    del user._sa_instance_state
    return jsonify({
        'status': 'OK',
        'user': user.to_dict()
    })

# CREATE -------------------

def create_new_user(request):
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
    del new_user._sa_instance_state
    from models.auth.token import Token
    new_token = Token(new_user.id, new_user.access_token)
    new_token.save()
    del new_token._sa_instance_state
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