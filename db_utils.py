import logging
import sqlite3
import os

log = logging.getLogger(__name__)

DB_NAME = './books.db'

IntegrityError = sqlite3.IntegrityError


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
        books = [('I Robot', 'Isaac Asimov'),
                 ('React to Python', 'Sheehan'),
                 ('Zen and the Art of Motorcycle Maintenance', 'Robert Pirsig'),
                 ('Cosmos', 'Carl Sagan'),
                 ('The Contrary Farmer', 'Gene Logsdon')]
        for title, author in books:
            execute(f"INSERT INTO Books(title, author) values(?, ?)", (title, author))
