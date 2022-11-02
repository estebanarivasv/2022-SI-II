from Crypto.PublicKey import RSA
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt)

from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
_user_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")


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
            # ACA CREAMOS Y GUARDAMOS EN CADA USUARIO, SU CLAVE PUBLICA Y CLAVE PRIVADA
            new_key = RSA.generate(1024, e=65537)
            new_user.public_key = new_key.exportKey("PEM")
            new_user.private_key = new_key.publickey().exportKey("PEM")

            new_user.save_to_db()
            return {'message': 'User {} was created'.format(data['username'])}
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
            return {
                'access_token': access_token
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
    @jwt_required()
    def get(self):
        return {'message': 'Aca vamos a devolver el perfil del usuario'}, 200
