<<<<<<< HEAD
=======
import os
>>>>>>> feature/filter-hoteis
from flask import Flask, jsonify
from flask_restful import Api

from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserAll, UserLogout
from flask_jwt_extended import JWTManager

<<<<<<< HEAD
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACY_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '58280d9e-60b3-11eb-ae93-0242ac130002'
=======

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACY_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
>>>>>>> feature/filter-hoteis
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity['role']


@jwt.token_in_blacklist_loader
def verify_blacklist(identity):
    return identity['jti'] in BLACKLIST


@jwt.revoked_token_loader
def access_token_invalidated():
    return jsonify({'message': 'You have been logged out.'}), 401


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserAll, '/usuarios/all')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import db

    db.init_app(app)
    app.run(debug=True)
