from flask import Blueprint, Response
from flask_restful import Resource, Api, reqparse
import flask_login
import logging
import sqlite3
import os

log = logging.getLogger(__name__)

DB_NAME = './data.db'

db_api = Blueprint('db_api', __name__, url_prefix='/api')


def execute(stmt, params=()):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()
            curs.execute(stmt, params)
            rowcount = curs.rowcount
            curs.close()
            conn.commit()
        return rowcount
    except Exception as e:
        log.error(str(e))
        raise


def select(stmt, params=()):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()
            curs.execute(stmt, params)
            desc = curs.description
            cols = [fld[0] for fld in desc]
            rowset = curs.fetchall()
            rows = [dict(zip(cols, row)) for row in rowset]
            curs.close()
        return rows
    except Exception as e:
        log.error(str(e))
        raise


def db_init():
    # Create the database if it doesn't exist
    if not os.path.exists(DB_NAME):
        log.warning("Creating new DB")

        execute("CREATE TABLE Books ("
                "id INTEGER PRIMARY KEY NOT NULL, "
                "title TEXT UNIQUE, "
                "author TEXT)")

        # Populate with test data
        books = {'I Robot': 'Asimov',
                 'React to Python': 'Sheehan',
                 'Zen and the Art of Motorcycle Maintenance': 'Pirsig',
                 'Cosmos': 'Sagan',
                 'The Contrary Farmer': 'Logsdon'}
        for title, author in books.items():
            execute(f"INSERT INTO Books(title, author) values(?, ?)", (title, author))


class Books(Resource):
    @staticmethod
    def get():
        records = select('SELECT id, title, author FROM Books')
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

            result = execute('INSERT INTO BOOKS (title, author) VALUES(?, ?)', (title, author))
            if result == 1:
                return Response("OK", 201)
            else:
                return Response("Bad Request", 400)
        except sqlite3.IntegrityError:
            return Response(f"Title '{title}' already exists!", 409)
        except Exception as e:
            log.error(str(e))
            return Response("Bad Request", 400)


class Book(Resource):
    @staticmethod
    def get(book_id):
        records = select('SELECT id, title, author FROM Books WHERE id = ?', (book_id,))
        return {'book': records[0] if len(records) > 0 else None}

    @flask_login.login_required
    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('author', type=str)
        args = parser.parse_args()
        title = args.get('title')
        author = args.get('author')

        result = execute('UPDATE BOOKS SET title=?, author=? WHERE id=?', (title, author, book_id))
        if result == 1:
            return Response("OK", 200)
        else:
            return Response(f"ID {book_id} does not exist!", 404)

    @flask_login.login_required
    def delete(self, book_id):
        try:
            result = execute('DELETE FROM BOOKS WHERE id=?', (book_id,))
            if result == 1:
                return Response("OK", 204)
            else:
                return Response(f"ID {book_id} does not exist!", 404)
        except Exception as e:
            log.error(str(e))


api = Api(db_api)
api.add_resource(Book, '/books/<int:book_id>')
api.add_resource(Books, '/books')
