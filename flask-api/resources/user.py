from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt)

from models.user import UserModel, Message
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
_user_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

_message_parser = reqparse.RequestParser()
_message_parser.add_argument('text', type=str, required=True, help="This field cannot be blank.")
_message_parser.add_argument('receiver', type=str, required=True, help="This field cannot be blank.")


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
            new_user.private_key = new_key.exportKey("PEM")
            new_user.public_key = new_key.publickey().exportKey("PEM")

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
    # TODO: PABLO FRACARO, ESTO ES TUYO.
    @jwt_required()
    def get(self):
        return {'message': 'Aca vamos a devolver el perfil del usuario'}, 200


class UserSendMail(Resource):
    @jwt_required()
    def post(self):
        user_sender = UserModel.find_by_username(get_jwt()['sub'])

        data = _message_parser.parse_args()
        if data['receiver'] == '' or data['text'] == '':
            return {'message': 'Missing data'}, 400

        user_receiver = UserModel.find_by_username(data['receiver'])

        if not user_receiver:
            return {'message': 'User {} doesn\'t exist'.format(data['receiver'])}

        cipher_encrypt = PKCS1_OAEP.new(RSA.importKey(user_receiver.public_key))

        # cipher_decrypt = PKCS1_OAEP.new(RSA.importKey(user_receiver.private_key)) DECRYPT

        encrypted_text = cipher_encrypt.encrypt(data['text'].encode('utf-8'))

        # print("test2: ", cipher_decrypt.decrypt(encrypted_text)) DECRYPT

        new_msg = Message(
            text=str(encrypted_text),
            sender=user_sender.username,
            receiver=user_receiver.username
        )

        try:
            new_msg.save_to_db()
            return {'message': 'Message sent'}
        except:
            return {'message': 'Something went wrong'}, 500
