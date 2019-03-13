from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, save_user_class, get_user_class#, get_all_users, get_a_user
from app.main.service.auth_helper import Auth
from ..util.decorator import token_required

api = UserDto.api
_user = UserDto.user
_user_class = UserDto.user_class
parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers', required=True)


@api.route('')
class User(Resource):
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        return save_new_user(data=request.json)

@api.route('/class')
class UserClass(Resource):
    @api.response(200, 'User class, specialization, items successfully saved.')
    @api.doc('save class, specialization, items', parser=parser, body=_user_class)
    @token_required
    def put(self, user_id):
        """Saves user's class, specialization, items"""
        return save_user_class(user_id, request.json)

@api.route('/class/<class_id>/<specialization_id>')
@api.param('class_id', 'User Class Identifier')
@api.param('specialization_id', 'User Class Specialization Identifier')
@api.response(404, 'User Class not found.')
class UserClassList(Resource):    
    @api.doc('get specializations, items of class', parser=parser)
    @api.marshal_with(_user_class)
    @token_required
    def get(self, user_id, class_id, specialization_id):
        """Gets user's specializations, items of class"""
        user_class = get_user_class(user_id, class_id, specialization_id)
        if not user_class:
            api.abort(404)
        else:
            return user_class
