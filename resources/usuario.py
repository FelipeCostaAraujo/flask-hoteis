from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt

from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.usuario import UserModel
from flask_restful import Resource, reqparse

from resources.jwt_admin_required import admin_required

attributes = reqparse.RequestParser()
attributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
attributes.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")
attributes.add_argument('role', type=str, required=False)


class User(Resource):

    @staticmethod
    def get(user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @admin_required
    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except ():
                return {'message': 'An error ocurred trying to delete user.'}, 500
            return {'message': 'user deleted'}, 200
        return {'message': 'user not found'}, 404


class UserRegister(Resource):
    @staticmethod
    def post():
        dados = attributes.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists".format(dados['login'])}
        if dados.role is None:
            dados.role = "user"
        user = UserModel(**dados)
        user.save_user()
        return {"message": "User created successfully!"}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = attributes.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.json())
            return {'access_token': token_de_acesso, 'user': user.json()}, 200
        return {'message': 'The username or password is incorrect'}, 401


class UserAll(Resource):
    @admin_required
    @jwt_required
    def get(self):
        return [user.json() for user in UserModel.query.all()]


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}
