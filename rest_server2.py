from flask import Flask, request, Response
from flask_restful import Resource, Api
import logging
import os

from db_utils import db_init, select

fmt = "[%(asctime)s]|%(levelname)s|[%(module)s]:%(funcName)s()|%(message)s"
logging.basicConfig(format=fmt)
log = logging.getLogger()
log.setLevel(logging.INFO)

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(16))


@app.errorhandler(404)
def request_not_found(err):
    return Response('NOT FOUND', 404)


@app.before_request
def request_log():
    log.info(f"[{request.method}] {request.full_path}")


@app.route('/', methods=['GET'])
def index():
    return Response("OK", 200)


class Books(Resource):
    @staticmethod
    def get():
        records = select('SELECT id, title, author FROM Books')
        return {'books': records if len(records or '') > 0 else []}


class Book(Resource):
    @staticmethod
    def get(book_id):
        records = select('SELECT id, title, author FROM Books WHERE id = ?', (book_id,))
        return {'book': records[0] if len(records) > 0 else None}


api = Api(app)
api.add_resource(Book, '/api/books/<int:book_id>')
api.add_resource(Books, '/api/books')

if __name__ == "__main__":
    db_init()
    app.run(host='0.0.0.0', port=8000, debug=True)
