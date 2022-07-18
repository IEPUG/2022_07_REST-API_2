from flask import Flask, request, Response
import logging
import os

from db_routes3 import db_api
from db_utils import db_init

fmt = "[%(asctime)s]|%(levelname)s|[%(module)s]:%(funcName)s()|%(message)s"
logging.basicConfig(format=fmt)
log = logging.getLogger()
log.setLevel(logging.INFO)

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(16))

app.register_blueprint(db_api)


@app.errorhandler(404)
def request_not_found(err):
    return Response('NOT FOUND', 404)


@app.before_request
def request_log():
    log.info(f"[{request.method}] {request.full_path}")


@app.route('/', methods=['GET'])
def index():
    return Response("OK", 200)


if __name__ == "__main__":
    db_init()
    app.run(host='0.0.0.0', port=8000, debug=True)
