from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


# configuration
DEBUG = True

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

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Book {self.name}>'

    def to_dict(self):
        data = {
            'book_id': self.book_id,
            'name': self.name,
            'description': self.description,
            'authors': [{'id': x.author_id, 'name': x.name} for x in self.authors]
        }
        return data


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
            'books': [{'id': x.book_id, 'name': x.name} for x in self.books]
        }
        return data

db.create_all()

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    print(request.get_json())
    return jsonify('pong!')


@app.route('/authors', methods=['GET'])
def authors_get():
    author_id = request.args.get('id')
    if author_id is None:
        authors = [x.to_dict() for x in Author.query.all()]
        response = {'authors': authors}
    else:
        response = Author.query.get_or_404(author_id).to_dict()
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
    pass

@app.route('/authors', methods=['DELETE'])
def authors_delete():
    pass



@app.route('/books', methods=['GET'])
def books_get():
    book_id = request.args.get('id')
    if book_id is None:
        books = [x.to_dict() for x in Book.query.all()]
        response = {'books': books}
    else:
        response = Book.query.get_or_404(book_id).to_dict()
    return jsonify(response)

@app.route('/books', methods=['POST'])
def books_post():
    print(1)
    data = request.get_json()
    print(data)
    b = Book(**data['book'])
    db.session.add(b)

    a = Author.query.get_or_404(data['author_id'])
    a.books.append(b)
    db.session.commit()
    response = {'success': True}
    return jsonify(response)

@app.route('/books', methods=['PUT'])
def books_put():
    pass

@app.route('/books', methods=['DELETE'])
def books_delete():
    pass




@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()