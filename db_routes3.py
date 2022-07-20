from flask import Blueprint
from flask_restful import Resource, Api
import logging

import db_utils as db

log = logging.getLogger(__name__)

db_api = Blueprint('db_api', __name__, url_prefix='/api')


class Books(Resource):
    @staticmethod
    def get():
        records = db.select('SELECT id, title, author FROM Books')
        return {'books': records if len(records) > 0 else []}


class Book(Resource):
    @staticmethod
    def get(book_id):
        records = db.select('SELECT id, title, author FROM Books WHERE id = ?', (book_id,))
        return {'book': records[0] if len(records) > 0 else None}


api = Api(db_api)
api.add_resource(Book, '/books/<int:book_id>')
api.add_resource(Books, '/books')
