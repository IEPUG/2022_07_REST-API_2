from flask import Flask, jsonify, request, Response, session
import flask_login
import logging
import os
from datetime import timedelta

from admin_routes import admin_api, User
from db_routes import db_api, db_init

fmt = "[%(asctime)s]|%(levelname)s|[%(module)s]:%(funcName)s()|%(message)s"
logging.basicConfig(format=fmt)
log = logging.getLogger()
log.setLevel(logging.INFO)

SESSION_TIMEOUT = 60

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.config.update(SECRET_KEY=os.urandom(16))
app.permanent_session_lifetime = timedelta(minutes=SESSION_TIMEOUT)

app.register_blueprint(db_api)
app.register_blueprint(admin_api)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    log.warning(f"UNAUTHORIZED [{request.method}] {request.full_path}")
    return Response("UNAUTHORIZED", 401)


@app.errorhandler(404)
def request_not_found(err):
    return jsonify({'error': str(err)})


@app.before_request
def request_log():
    log.info(f"[{request.method}] {request.full_path}")


@app.before_request
def refresh_session():
    session.modified = True


@app.route('/', methods=['GET'])
def index():
    return Response("OK", 200)


if __name__ == "__main__":
    db_init()
    app.run(host='0.0.0.0', port=8000, debug=True)
