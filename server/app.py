from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy


# configuration
PAGINATE_VALUE = 3

# instantiate the app
app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

books = db.Table('books',
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id'), primary_key=True)
)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    rating = db.Column(db.Float(), default=.0)
    count_marks = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Book {self.name}>'

    def to_dict(self):
        data = {
            'book_id': self.book_id,
            'name': self.name,
            'description': self.description,
            'authors': [{'id': x.author_id, 'name': x.name} for x in self.authors],
            'rating': self.rating,
        }
        return data

    def delete(self):
        pass


class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    sername = db.Column(db.String(80), unique=False, nullable=True)

    books = db.relationship('Book', secondary=books, lazy='subquery',
        backref=db.backref('authors', lazy=True))

    def __init__(self, **kwargs):
        super(Author, self).__init__(**kwargs)
    
    def __repr__(self):
        return f'<Author {self.name}>'

    def to_dict(self):
        data = {
            'author_id': self.author_id,
            'name': self.name,
            'sername': self.sername,
            'books': [
                {'id': x.book_id, 'name': x.name}
                for x
                in sorted(self.books, key=lambda x: x.rating, reverse=True)[:5]
            ]
        }
        return data


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/authors', methods=['GET'])
def authors_get():
    author_id = request.args.get('id')

    if author_id is not None and author_id.isdigit():
        response = Author.query.get_or_404(author_id).to_dict()
    else:
        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        authors = Author.query.filter().paginate(
            page=page,
            per_page=PAGINATE_VALUE
        )
        response = {
            'authors': [x.to_dict() for x in authors.items],
            'pagination': {
                'has_next': authors.has_next,
                'has_prev': authors.has_prev,
                'next_num': authors.next_num,
                'prev_num': authors.prev_num,
                'pages': authors.pages
            }
        }
    return jsonify(response)

@app.route('/authors', methods=['POST'])
def authors_post():
    data = request.get_json()
    a = Author(**data)
    db.session.add(a)
    db.session.commit()
    response = {'success': True}
    return jsonify(response)


@app.route('/authors', methods=['PUT'])
def authors_put():
    data = request.get_json()
    a = Author.query.filter_by(author_id=data['author_id']).first()
    list_b = Book.query.filter(Book.book_id.in_(data['book_id']))
    for b in list_b:
        b.authors.append(a)
    db.session.commit()
    response = {'success': True}
    return jsonify(response)


@app.route('/authors', methods=['DELETE'])
def authors_delete():
    pass



@app.route('/books', methods=['GET'])
def books_get():
    book_id = request.args.get('id')

    if book_id is not None and book_id.isdigit():
        response = Book.query.get_or_404(book_id).to_dict()
    else:
        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        books = Book.query.filter().paginate(
            page=page,
            per_page=PAGINATE_VALUE
        )
        books = [x.to_dict() for x in books.items]
        response = {'books': books}
    return jsonify(response)

@app.route('/books', methods=['POST'])
def books_post():
    data = request.get_json()
    b = Book(**data['book'])
    list_a = Author.query.filter(Author.author_id.in_(data['author_id']))
    for a in list_a:
        a.books.append(b)
    db.session.add(b)
    db.session.commit()
    response = {'success': True}
    return jsonify(response)

@app.route('/books', methods=['PATCH'])
def books_patch():
    data = request.get_json()
    b = Book.query.filter_by(book_id=data['id']).first()
    b.count_marks += 1
    b.rating = (b.rating * (b.count_marks - 1) + data['rating']) / b.count_marks
    db.session.add(b)
    db.session.commit()
    response = {'rating': b.rating}
    return jsonify(response)

@app.route('/books', methods=['PUT'])
def books_put():
    data = request.get_json()
    b = Book.query.filter_by(book_id=data['id']).first()
    list_a = Author.query.filter(Author.author_id.in_(data['author_id']))
    for a in list_a:
        a.books.append(b)
    db.session.add(b)
    db.session.commit()
    response = {'success': True}
    return jsonify(response)

@app.route('/books', methods=['DELETE'])
def books_delete():
    pass


db.create_all()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run()