from flask import Response, session, Blueprint
from flask_restful import Api, Resource, reqparse
from werkzeug.security import check_password_hash, generate_password_hash
import flask_login
import logging


log = logging.getLogger(__name__)

admin_api = Blueprint('admin_api', __name__, url_prefix='/api')


class User(flask_login.UserMixin):
    def __init__(self, userid):
        self.id = userid


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        username = args.get('username').lower()
        pwd = args.get('password')

        if self.validateLogin(username, pwd):
            flask_login.login_user(User(username))
            session.permanent = True
            return Response("OK", 200)
        else:
            log.warning(f"Failed login attempt for user '{username}'")
            flask_login.logout_user()
            return Response("UNAUTHORIZED", 401)

    @staticmethod
    def validateLogin(user, pwd):
        # TODO: Use db.user table for user validation
        SECRET_PASSWORD = generate_password_hash('123')
        return user == 'admin' and check_password_hash(SECRET_PASSWORD, pwd)


class Logout(Resource):
    @staticmethod
    @flask_login.login_required
    def get():
        flask_login.logout_user()
        return Response("OK", 200)


class GetUser(Resource):
    @staticmethod
    @flask_login.login_required
    def get():
        user = ''
        if flask_login.current_user.is_authenticated:
            user = flask_login.current_user.get_id()
        return {'user': user}


class KeepAlive(Resource):
    @staticmethod
    @flask_login.login_required
    def get():
        return Response("OK", 200)


api = Api(admin_api)
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(GetUser, '/whoami')
api.add_resource(KeepAlive, '/ping')
