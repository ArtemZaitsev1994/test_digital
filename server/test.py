import sys
sys.path.append("..")

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
        for i in range(10):
            db.session.add(Author(**{'name': 'Default', 'sername': 'Author'}))
        for i in range(10):
            db.session.add(Book(**{'name': 'Default', 'description': 'Book'}))
        db.session.flush()
        
        a = Author.get_one_item(1)
        b = Book.get_one_item(1)
        a.books.append(b)
        db.session.add(a)
        
        a2 = Author.get_one_item(2)
        a2.books.extend([Book.get_one_item(x) for x in range(1, 11)])
        db.session.add(a2)

        db.session.flush()
        db.session.expunge_all()

    def test_messages(self):
        rv = self.app.get('/ping', follow_redirects=True)
        assert rv.status == '200 OK'

    def test_create_author(self):
        """Тест создания автора книг."""

        data = {'name': 'Artem', 'sername': 'Zaitsev'}
        rv = self.app.post('/authors', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'
        assert len(Author.query.all()) == 11
        a = Author.get_one_item(11)
        assert a.name == data['name'] 
        assert a.sername == data['sername'] 
        assert len(a.books) == 0
    
    def test_negative_create_author(self):
        """Негативный тест создания автора книг."""

        data = {'name': 1}
        rv = self.app.post('/authors', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'
        # assert len(Author.get_all()) == 10

        data = {'sername': 1}
        rv = self.app.post('/authors', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'
        # assert len(Author.get_all()) == 10
        
    def test_create_book(self):
        """Тест создания книги. Книга не может быть создана без автора."""
        data = {
            'book': {
                'name': 'Kolobok',
                'description': 'The story about bread.'
            },
            'author_id': [1, 2]
        }
        rv = self.app.post('/books', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'
        b = Book.get_one_item(11)
        assert b.name == data['book']['name']
        assert len(b.authors) == 2

        a1 = Author.get_one_item(1)
        assert a1 in b.authors
        a2 = Author.get_one_item(2)
        assert a2 in b.authors

    def test_negative_book_create(self):
        """Негативный тест создания книги."""
        assert len(Book.query.all()) == 10
        
        data = {
            'book': {
                'name': 'Kolobok',
                'Description': 'The story about bread.'
            },
            'authors': []
        }
        rv = self.app.post('/books', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

    def test_add_book_to_author(self):
        """Тест на добавление книги к автору."""

        a = Author.get_one_item(3)
        assert len(a.books) == 0

        data = {"author_id": 3, "book_id": [1]}
        rv = self.app.put('/authors', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'

        a = Author.get_one_item(3)
        assert len(a.books) == 1

    def test_delete_book_from_author(self):
        """Тест на разрыв связи книги и автора."""

        a = Author.get_one_item(2)
        b = Book.get_one_item(1)
        assert b in a.books

        data = {"author_id": 2, "book_id": 1}
        rv = self.app.patch('/authors', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'

        a = Author.get_one_item(2)
        b = Book.get_one_item(1)
        assert b not in a.books

    def test_delete_book_from_author_negative(self):
        """Негативный тест на разрыв связи книги и автора."""

        data = {"author_id": 1, "book_id": 4}
        rv = self.app.patch('/authors', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

        data = {"author_id": 1, "book_id": 1}
        rv = self.app.patch('/authors', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

        data = {"author_id": 6, "book_id": 1}
        rv = self.app.patch('/authors', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

    def test_add_book_to_author_negative(self):
        """Негативный тест на добавление книги к автору."""

        data = {"author_id": 12, "book_id": [1]}
        rv = self.app.put('/authors', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

    def test_add_author_to_book(self):
        """Тест на добавление авторов к книге."""

        b = Book.get_one_item(2)
        assert len(b.authors) == 1

        data = {"book_id": 2, "author_id": [3]}
        rv = self.app.put('/books', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'

        a = Author.get_one_item(3)
        b = Book.get_one_item(2)
        assert b in a.books
        assert a in b.authors
        assert len(b.authors) == 2

    def test_add_author_to_book_negative(self):
        """Негативный тест на добавление авторов к книге."""

        b = Book.get_one_item(3)
        assert len(b.authors) == 1

        data = {"book_id": 2, "author_id": [22]}
        rv = self.app.put('/books', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

    def test_change_book_rating(self):
        """Тест на изменение рейтинга книги."""

        b = Book.get_one_item(1)
        assert b.rating == 0
        assert b.count_marks == 0

        data = {"book_id": 1, "rating": 5}
        rv = self.app.patch('/books', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'

        b = Book.get_one_item(1)
        assert b.rating == 5
        assert b.count_marks == 1

        data = {"book_id": 1, "rating": 5}
        rv = self.app.patch('/books', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'

        b = Book.get_one_item(1)
        assert b.rating == 5
        assert b.count_marks == 2

        data = {"book_id": 1, "rating": 2}
        rv = self.app.patch('/books', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'

        b = Book.get_one_item(1)
        assert b.rating == 4
        assert b.count_marks == 3

        data = {"book_id": 1, "rating": 2}
        rv = self.app.patch('/books', json=data)
        json_resp = rv.get_json()
        assert json_resp['success']
        assert rv.status == '200 OK'

        b = Book.get_one_item(1)
        assert b.rating == 3.5
        assert b.count_marks == 4

    def test_change_book_rating_negative(self):
        """Тест на изменение рейтинга книги."""

        b = Book.get_one_item(1)
        assert b.rating == 0
        assert b.count_marks == 0

        data = {"book_id": 1, "rating": 6}
        rv = self.app.patch('/books', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

        data = {"book_id": 1, "rating": 0}
        rv = self.app.patch('/books', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

        data = {"book_id": 1, "rating": 3.13541314}
        rv = self.app.patch('/books', json=data)
        json_resp = rv.get_json()
        assert not json_resp['success']
        assert rv.status == '200 OK'

    def test_get_author(self):
        """Тест на получение автора по ID."""
        from data_test import DATA_GET_AUTHOR_BY_ID

        a = Author.get_one_item(1)
        rv = self.app.get('/authors?id=1')
        json_resp = rv.get_json()
        assert json_resp == DATA_GET_AUTHOR_BY_ID
        assert rv.status == '200 OK'

    def test_get_list_of_authors(self):
        """Тест на получение списка авторов."""
        from data_test import GET_LIST_AUTHORS

        rv = self.app.get('/authors')
        json_resp = rv.get_json()
        assert json_resp['authors'] == GET_LIST_AUTHORS
        assert rv.status == '200 OK'

    def test_pagination_authors(self):
        """Тестирование работы пагинации при запросе авторов."""
        from data_test import DATA_TEST_AUTHORS_PAGINATION

        rv = self.app.get('/authors?pagin=2&page=3')
        json_resp = rv.get_json()
        assert json_resp['pagination'] == DATA_TEST_AUTHORS_PAGINATION
        assert rv.status == '200 OK'

    def test_pagination_books(self):
        """Тестирование работы пагинации при запросе книг."""
        from data_test import DATA_TEST_BOOKS_PAGINATION

        rv = self.app.get('/books?pagin=3&page=2')
        json_resp = rv.get_json()
        assert json_resp['pagination'] == DATA_TEST_BOOKS_PAGINATION
        assert rv.status == '200 OK'

    def test_get_book(self):
        """Тест на получение книги."""
        from data_test import DATA_GET_BOOK_BY_ID

        b = Author.get_one_item(1)
        rv = self.app.get('/books?id=1')
        json_resp = rv.get_json()
        assert json_resp == DATA_GET_BOOK_BY_ID
        assert rv.status == '200 OK'

    def test_get_list_of_books(self):
        """Тест на получение списка книг."""
        from data_test import DATA_GET_BOOK_LIST

        rv = self.app.get('/books?pagin=2&page=3')
        json_resp = rv.get_json()
        json_resp['books'] == DATA_GET_BOOK_LIST
        assert rv.status == '200 OK'

    def test_get_list_of_authors(self):
        """Тест на получение списка авторов."""

        self.app.patch('/books', json={"book_id": 4, "rating": 1})
        self.app.patch('/books', json={"book_id": 5, "rating": 2})
        self.app.patch('/books', json={"book_id": 6, "rating": 4})
        self.app.patch('/books', json={"book_id": 7, "rating": 3})
        self.app.patch('/books', json={"book_id": 8, "rating": 4})
        self.app.patch('/books', json={"book_id": 8, "rating": 3})
        self.app.patch('/books', json={"book_id": 9, "rating": 5})
        # (ID книги, оценка)
        result = [(9, 5.0), (6, 4.0), (8, 3.5), (7, 3.0), (5, 2.0)]

        rv = self.app.get('/authors')
        assert rv.status == '200 OK'
        json_resp = rv.get_json()
        # к автору с ID=2 привязаны все 10 дефолтных книг
        author = next((x for x in json_resp['authors'] if x['author_id'] == 2), None)
        assert author is not None

        books = [(x['book_id'], x['rating']) for x in author['books']]
        assert books == result


if __name__ == '__main__':
    unittest.main()
