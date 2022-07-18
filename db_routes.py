from flask import Blueprint, Response
from flask_restful import Resource, Api, reqparse
import flask_login
import logging

import db_utils as db

log = logging.getLogger(__name__)

DB_NAME = './data.db'

db_api = Blueprint('db_api', __name__, url_prefix='/api')


class Books(Resource):
    @staticmethod
    def get():
        records = db.select('SELECT id, title, author FROM Books')
        return {'books': records if len(records or '') > 0 else []}

    @flask_login.login_required
    def post(self):
        title = ''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('author', type=str)
            args = parser.parse_args()
            title = args.get('title')
            author = args.get('author')

            result = db.execute('INSERT INTO BOOKS (title, author) VALUES(?, ?)', (title, author))
            if result == 1:
                return Response("OK", 201)
            else:
                return Response("Bad Request", 400)
        except db.IntegrityError:
            return Response(f"Title '{title}' already exists!", 409)
        except Exception as e:
            log.error(str(e))
            return Response("Bad Request", 400)


class Book(Resource):
    @staticmethod
    def get(book_id):
        records = db.select('SELECT id, title, author FROM Books WHERE id = ?', (book_id,))
        return {'book': records[0] if len(records) > 0 else None}

    @flask_login.login_required
    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('author', type=str)
        args = parser.parse_args()
        title = args.get('title')
        author = args.get('author')

        result = db.execute('UPDATE BOOKS SET title=?, author=? WHERE id=?', (title, author, book_id))
        if result == 1:
            return Response("OK", 200)
        else:
            return Response(f"ID {book_id} does not exist!", 404)

    @flask_login.login_required
    def delete(self, book_id):
        try:
            result = db.execute('DELETE FROM BOOKS WHERE id=?', (book_id,))
            if result == 1:
                return Response("OK", 204)
            else:
                return Response(f"ID {book_id} does not exist!", 404)
        except Exception as e:
            log.error(str(e))


api = Api(db_api)
api.add_resource(Book, '/books/<int:book_id>')
api.add_resource(Books, '/books')
