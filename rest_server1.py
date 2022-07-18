from flask import Flask, Response
import logging
import os

from db_utils import db_init, select

fmt = "[%(asctime)s]|%(levelname)s|[%(module)s]:%(funcName)s()|%(message)s"
logging.basicConfig(format=fmt)
log = logging.getLogger()
log.setLevel(logging.INFO)

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(16))


@app.route('/', methods=['GET'])
def index():
    return Response("OK", 200)


@app.route('/api/books', methods=['GET'])
def books():
    records = select('SELECT id, title, author FROM Books')
    return {'books': records if len(records or '') > 0 else []}


@app.route('/api/books/<int:book_id>', methods=['GET'])
def book(book_id):
    records = select('SELECT id, title, author FROM Books WHERE id = ?', (book_id,))
    return {'book': records[0] if len(records) > 0 else None}


if __name__ == "__main__":
    db_init()
    app.run(host='0.0.0.0', port=8000, debug=True)
