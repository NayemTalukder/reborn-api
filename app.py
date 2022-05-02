import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from models.store import StoreModel
from resources.store import Store, Storelist
from resources.item import Item, Itemlist
from resources.home import Home
from resources.user import UserRegistration, UserLogin, UserLogoutAccess, UserLogoutRefresh, RevokedTokenModel, TokenRefresh, AllUsers, User

app = Flask(__name__)

app.config['SECRET_KEY']='Nayem'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


jwt = JWTManager(app)
api = Api(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

# @app.before_first_request
# def create_table():
#     db.create_all()

api.add_resource(Home, '/')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Itemlist, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Storelist, '/stores')

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(AllUsers, '/users')
api.add_resource(User, '/user/<string:name>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)