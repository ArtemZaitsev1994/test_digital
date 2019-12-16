import unittest

from app import app, db
from authors.blueprint import authors
from books.blueprint import books
from models import Author, Book


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/testing?charset=utf8'

        app.register_blueprint(authors)
        app.register_blueprint(books)
        self.app = app.test_client()

        db.create_all()
        self.fill_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def fill_db(self):
        a = [Author({'name': 'Default', 'sername': 'Author'}) for x in range(10)]
        b = [Book({'name': 'Default', 'Description': 'Book'}).save() for x in range(10)]
        a[0].books.append(b[0])
        a[1].books.extend(b)
        [x.save() for x in a]

    def test_messages(self):
        rv = self.app.get('/ping', follow_redirects=True)
        assert rv.status == '200 OK'

    def test_create_author(self):
        """Тест создания автора книг."""

        data = {'name': 'Artem', 'sername': 'Zaitsev'}
        rv = self.app.post('/authors', json=data)
        assert rv.status == '200 OK'
        assert len(Author.query.all()) == 11
        a = Author.get_one_user(11)
        assert a.name == data['name'] 
        assert a.sername == data['sername'] 
        assert len(a.books) == 0
    
    def test_negative_create_author(self):
        """Негативный тест создания автора книг."""

        assert len(Author.query.all()) == 10

        data = {'name': 1, 'sername': 'Zaitsev'}
        rv = self.app.post('/authors', json=data)
        assert rv.status == '200 OK'
        assert len(Author.query.all()) == 10

        data = {'name': 'Artem', 'sername': 1}
        rv = self.app.post('/authors', json=data)
        assert rv.status == '200 OK'
        assert len(Author.query.all()) == 10
        
    def test_create_book(self):
        """Тест создания книги. Книга не может быть создана без автора."""

        data = {'name': 'Kolobok', 'Description': 'The story about bread.', 'authors': [1, 2]}
        rv = self.app.post('/books', json=data)
        assert rv.status == '200 OK'
        assert len(Book.query.all()) == 10
        b = Book.get_one_user(11)
        assert b.name == data['name']
        assert len(b.authors) == 2

        a1 = Author.get_one_user(1)
        assert a1 in b.authors
        a2 = Author.get_one_user(2)
        assert a2 in b.authors

    def test_negative_book_create(self):
        """Негативный тест создания книги."""

        assert len(Book.query.all()) == 10

        data = {'name': 'Kolobok', 'Description': 'The story about bread.', 'authors': []}
        rv = self.app.post('/books', json=data)
        assert rv.status == '200 OK'
        assert len(Book.query.all()) == 10

    def test_add_book_to_author(self):
        """Тест на добавление книги к автору."""

        a2 = Author.get_one_user(3)
        assert len(a2.books) == 0

        data = {"author_id": 3, "book_id": [1]}
        rv = self.app.put('/authors', json=data)
        assert rv.status == '200 OK'
        b = Book.get_one_user(2)
        assert b in a2.books

    def test_add_book_to_author_negative(self):
        """Негативный тест на добавление книги к автору."""

        a2 = Author.get_one_user(2)
        assert len(a2.books) == 0

        data = {"author_id": 12, "book_id": [1]}
        rv = self.app.put('/authors', json=data)
        assert rv.status == '200 OK'
        assert len(a2.books) == 0

    def test_add_author_to_book(self):
        """Тест на добавление авторов к книге."""

        b = Book.get_one_user(2)
        assert len(b.authors) == 1

        data = {"book_id": 2, "author_id": [3]}
        rv = self.app.put('/books', json=data)
        assert rv.status == '200 OK'

        a2 = Author.get_one_user(3)
        assert a2 in b.authors

    def test_add_author_to_book_negative(self):
        """Негативный тест на добавление авторов к книге."""

        b = Book.get_one_user(3)
        assert len(b.authors) == 0

        data = {"book_id": 2, "author_id": [22]}
        rv = self.app.put('/books', json=data)
        assert rv.status == '200 OK'
        assert len(b.authors) == 0

    def test_change_book_rating(self):
        """Тест на изменение рейтинга книги."""

        b = Book.get_one_user(1)
        assert b.rating == 0
        assert b.count_marks == 0

        data = {"book_id": 1, "rating": 5}
        rv = self.app.patch('/books', json=data)
        assert rv.status == '200 OK'

        assert b.rating == 5
        assert b.count_marks == 1

        data = {"book_id": 1, "rating": 5}
        rv = self.app.patch('/books', json=data)
        assert rv.status == '200 OK'

        assert b.rating == 5
        assert b.count_marks == 2

        data = {"book_id": 1, "rating": 2}
        rv = self.app.patch('/books', json=data)
        assert rv.status == '200 OK'

        assert b.rating == 4
        assert b.count_marks == 3

        data = {"book_id": 1, "rating": 2}
        rv = self.app.patch('/books', json=data)
        assert rv.status == '200 OK'

        assert b.rating == 3.5
        assert b.count_marks == 4

    def test_change_book_rating_negative(self):
        """Тест на изменение рейтинга книги."""

        b = Book.get_one_user(1)
        assert b.rating == 0
        assert b.count_marks == 0

        data = {"book_id": 1, "rating": 6}
        rv = self.app.patch('/books', json=data)
        assert rv.status == '200 OK'

        data = {"book_id": 1, "rating": 0}
        rv = self.app.patch('/books', json=data)
        assert rv.status == '200 OK'

        data = {"book_id": 1, "rating": 3.13541314}
        rv = self.app.patch('/books', json=data)
        assert rv.status == '200 OK'

    def test_get_author(self):
        """Тест на получение авторов."""
        pass

    def test_get_list_of_authors(self):
        """Тест на получение списка авторов."""
        pass

    def test_get_book(self):
        """Тест на получение пользователя."""
        pass

    def test_get_list_of_books(self):
        """Тест на получение списка пользователей."""
        pass









if __name__ == '__main__':
    unittest.main()



# def test_example(client):
#     response = client.get('/')
#     assert response.status_code == 200

# def test_create_author(client):
#     data = {'name': 'Artem', 'sername': 'Zaitsev'}
#     response = client.post('/authors', json=data)
#     assert response.status_code == 200








# # test_hello_add.py
# from app import app
# from flask import json


# def test_add():        
#     response = app.test_client().get('/')

#     data = json.loads(response.get_data(as_text=True))

#     print(data)
#     assert response.status_code == 200



# import pytest
# from flask import Flask, jsonify, request
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from sqlalchemy.exc import ProgrammingError

# from authors.blueprint import authors
# from books.blueprint import books
# from models import Book
# from models import Author, books as m2m_books




# # App Factory
# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/testing?charset=utf8'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     @app.route('/', methods=['POST', 'GET'])
#     def root():
#         return jsonify('pong')

#     with app.app_context():
#         db = SQLAlchemy()
#         db.init_app(app)
#         app.register_blueprint(authors)
#         app.register_blueprint(books)

#     return app


# # from yourapp.app.app import create_app
# # from yourapp.app.db import db as _db
# _db = SQLAlchemy()

# @pytest.yield_fixture(scope='session')
# def app():
#     _app = create_app()
#     ctx = _app.app_context()
#     ctx.push()

#     yield _app

#     ctx.pop()


# @pytest.fixture(scope='session')
# def testapp(app):
#     return app.test_client()


# @pytest.yield_fixture(scope='session')
# def db(app):
#     _db.app = app
#     _db.create_all()
#     _db.session.commit()

#     yield _db

#     _db.drop_all()
#     _db.session.commit()


# @pytest.fixture(scope='function', autouse=True)
# def session(db):
#     connection = db.engine.connect()
#     transaction = connection.begin()

#     options = dict(bind=connection, binds={})
#     session_ = db.create_scoped_session(options=options)

#     db.session = session_

#     yield session_

#     transaction.rollback()
#     connection.close()
#     session_.remove()



# @pytest.yield_fixture
# def app():
#     def _app():
#         app = create_app()
#         app.test_request_context().push()
#         db.init_app(app)
#         try:
#             Author.__table__.create(db.engine)
#         except ProgrammingError:
#             pass
#         try:
#             Book.__table__.create(db.engine)
#         except ProgrammingError:
#             pass
#         try:
#             m2m_books.create(db.engine)
#         except ProgrammingError:
#             pass

#         return app

#     yield _app()

#     m2m_books.drop(db.engine)
#     Author.__table__.drop(db.engine)
#     Book.__table__.drop(db.engine)


# @pytest.fixture
# def app():
#     app = create_app()
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()

# def test_example(client):
#     response = client.get('/')
#     assert response.status_code == 200

# def test_create_author(client):
#     data = {'name': 'Artem', 'sername': 'Zaitsev'}
#     response = client.post('/authors', json=data)
#     assert response.status_code == 200


# # async def test_delete_contact(cli):
# #     """Тест на удаление контакта у пользователя"""
# #     data = {
# #         'user_name': 'Artem',
# #         'contact': 'Sasha',
# #     }
# #     resp = await cli.delete('/api/contacts', json=data)
# #     assert resp.status == 200
# #     answer = json.loads(await resp.text())
# #     assert answer['success'] is True
# #     assert await User(cli.app.db, 'Artem').get_contacts() == {
# #         'Ivan' : {
# #             'telegram': 'Ivanov',
# #             'whatsApp': '+79508465333',
# #             'viber': 'viber_id',
# #         },

# #     }


# # async def test_send_message_to_messengers(cli):
# #     """Тест на отправку сообщения в мессенджеры"""
# #     HOST = 'http://0.0.0.0:8081/'
# #     adresses = {
# #         'telegram': f'{HOST}telegram',
# #         'whatsApp': f'{HOST}whatsapp',
# #         'viber': f'{HOST}viber'
# #     }
# #     redis_data = [{
# #         'sender': 'Artem',
# #         'message': 'Тест отправки сообщения в мессенджеры.',
# #         'contact': 'Ivan',
# #         'url': '',
# #         'time': [2019, 12, 1, 16, 41, 22]
# #     },
# #     {
# #         'sender': 'Artem',
# #         'message': 'Тест отправки сообщения в мессенджеры.',
# #         'contact': 'Sasha',
# #         'url': '',
# #         'time': None
# #     }]
# #     for t in redis_data:
# #         for adr in adresses.values():
# #             t['url'] = adr
# #             key = str(uuid.uuid4())
# #             await cli.app['redis'].set(key, json.dumps(t))
# #             await send_to_messenger(cli.app, t, key)
# #     assert await cli.app['redis'].scard('user_Artem') == 2
# #     await cli.app['redis'].flushdb()    


# # async def test_send_delayed_message_to_messengers(cli):
# #     """Тест на отправку отложенного (на 10 секунд) сообщения в мессенджеры"""
# #     planned_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
# #     data = {
# #         'sender': 'Artem',
# #         'message': 'Тест отправки сообщения в мессенджеры.',
# #         'contact': 'Ivan',
# #         'url': 'http://0.0.0.0:8081/whatsapp',
# #         'time': [
# #             planned_time.year,
# #             planned_time.month,
# #             planned_time.day,
# #             planned_time.hour,
# #             planned_time.minute,
# #             planned_time.second,
# #         ]
# #     }
# #     key = str(uuid.uuid4())
# #     await cli.app['redis'].set(key, json.dumps(data))
# #     await send_to_messenger(cli.app, data, key)
# #     assert datetime.datetime.now() + datetime.timedelta(seconds=1) > planned_time
# #     await cli.app['redis'].flushdb()