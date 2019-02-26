from flask_restplus import Namespace, fields

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'login_id': fields.String(required=True, description='user login id'),
        'password': fields.String(required=True, description='user password'),
    })
    user_class = api.model('user_class', {
        'class_id': fields.Integer(require=True, description = 'class id'),
        'specialization_id': fields.Integer(require=True, description = 'specialization id'),
        'item_ids': fields.List(fields.Integer, description="list of item ids"),
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'login_id': fields.String(required=True, description='The user login id'),
        'password': fields.String(required=True, description='The user password '),
    })

class ItemDto:
    api = Namespace('item', description='item related operations')

class MetaDto:
    api = Namespace('meta', description='meta data related operations')