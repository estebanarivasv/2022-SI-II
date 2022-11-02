from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt, verify_jwt_in_request
)
from six import wraps

from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            return {
                'message': 'User {} was created'.format(data['username']),
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  # jti is "JWT ID"
        BLACKLIST.add(jti)
        return {'Message': 'Successfully logged out.'}, 200


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'Message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'Message': 'User not found'}, 404
        user.delete_from_db()
        return {'Message': 'User deleted.'}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200



