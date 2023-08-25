import sys, os
from uuid import uuid4
from datetime import datetime

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

# import psycopg2

sys.path.append(sys.path[0] + "/..")
from src.app.models import Author, Book
from src.config import DB_HOST_TEST, DB_NAME_TEST, DB_USER_TEST, DB_PASS_TEST


@pytest.fixture
def create_table():
    dsn = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"
    engine = create_engine(dsn)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.execute(
        text(
            """
        DROP TABLE IF EXISTS book;
        DROP TABLE IF EXISTS author;
        """
        )
    )

    session.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS author (
                id UUID PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                fullname VARCHAR(100));
        """
        )
    )

    session.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS book (
                id UUID PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                author_id UUID REFERENCES author(id),
                date_of_release DATE DEFAULT CURRENT_DATE,
                description VARCHAR(300),
                genre VARCHAR(200) NOT NULL);
        """
        )
    )

    session.execute(
        text(
            """
        DELETE FROM author;
        DELETE FROM book;
        """
        )
    )

    session.execute(
        text(
            """
        INSERT INTO author VALUES ('a437623d-c141-464e-ae1a-ff2a13170cd7', 'Andrzej', 'Andrzej Sapkowski');
        INSERT INTO book VALUES 
        ('df6c4b45-23dd-4f60-89fe-10e75c516461', 'The Witcher', 'a437623d-c141-464e-ae1a-ff2a13170cd7',
         :date, 'Destiny', 'Fantasy')
        """
        ),
        {"date": datetime.now().date()},
    )

    session.commit()

    yield session

    session.close()


def test_read_db(create_table):
    session = create_table

    data = {
        "author_id": "a437623d-c141-464e-ae1a-ff2a13170cd7",
        "author_name": "Andrzej",
        "author_fullname": "Andrzej Sapkowski",
        "book_id": "df6c4b45-23dd-4f60-89fe-10e75c516461",
        "book_name": "The Witcher",
        "date_of_release": datetime.now().date(),
        "description": "Destiny",
        "genre": "Fantasy",
    }

    try:
        author = session.get(Author, data["author_id"])
        book = session.get(Book, data["book_id"])

        result = {
            "author_id": str(author.id),
            "author_name": author.name,
            "author_fullname": author.fullname,
            "book_id": str(book.id),
            "book_name": book.name,
            "date_of_release": book.date_of_release,
            "description": book.description,
            "genre": book.genre,
        }

    except:
        result = {}

    assert result == data


def test_write_db(create_table):
    session = create_table

    data = {
        "author_id": str(uuid4()),
        "author_name": "William",
        "author_fullname": "William Shakespeare",
        "book_id": "773e909e-f3d1-4b52-87b5-4d896e4c39b5",
        "book_name": "Romeo and Juliet",
        "date_of_release": datetime.now().date(),
        "description": "Love",
        "genre": "Drama",
    }

    try:
        author1 = Author(
            id=data["author_id"],
            name=data["author_name"],
            fullname=data["author_fullname"],
        )
        book1 = Book(
            id=data["book_id"],
            name=data["book_name"],
            author_id=data["author_id"],
            date_of_release=None,
            description=data["description"],
            genre=data["genre"],
        )

        session.add(author1)
        session.add(book1)
        session.commit()

        res1 = session.execute(
            text(
                """
            SELECT * FROM author WHERE id = :author_id 
            """
            ),
            data,
        ).first()

        res2 = session.execute(
            text(
                """
            SELECT * FROM book WHERE id = :book_id 
            """
            ),
            data,
        ).first()

        result = {
            "author_id": str(res1.id),
            "author_name": res1.name,
            "author_fullname": res1.fullname,
            "book_id": str(res2.id),
            "book_name": res2.name,
            "date_of_release": res2.date_of_release,
            "description": res2.description,
            "genre": res2.genre,
        }

    except:
        result = {}

    assert result == data
