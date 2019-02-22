from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, save_user_class, get_user_class#, get_all_users, get_a_user
from app.main.service.auth_helper import Auth
from ..util.decorator import token_required

api = UserDto.api
_user = UserDto.user
_user_class = UserDto.user_class


@api.route('/')
class User(Resource):
    # @api.doc('list_of_registered_users')
    # @api.marshal_list_with(_user, envelope='data')
    # @token_required
    # def get(self):
    #     """List all registered users"""
    #     return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        return save_new_user(data=request.json)

@api.route('/class')
class UserClass(Resource):
    @api.response(200, 'User class, specializations, items successfully saved.')
    @api.doc('save class, specializations, items')
    @api.expect(_user_class, validate=True)
    @token_required
    def put(self, user_id):
        """Saves user's class, specializations, items"""
        return save_user_class(user_id, request.json)

@api.route('/class/<class_id>')
@api.param('class_id', 'User Class Identifier')
@api.response(404, 'User Class not found.')
class UserClassList(Resource):    
    @api.doc('get specializations, items of class')
    @api.marshal_with(_user_class)
    @token_required
    def get(self, user_id, class_id):
        """Gets user's specializations, items of class"""
        user_class = get_user_class(user_id, class_id)
        if not user_class:
            api.abort(404)
        else:
            return user_class

# @api.route('/<login_id>')
# @api.param('login_id', 'The User identifier')
# @api.response(404, 'User not found.')
# class User(Resource):
#     @api.doc('get a user')
#     @api.marshal_with(_user)
#     @token_required
#     def get(self, login_id):
#         """get a user given its identifier"""
#         user = get_a_user(login_id)
#         if not user:
#             api.abort(404)
#         else:
#             return user