from app import db


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

    # def to_dict(self):
    #     data = {
    #         'book_id': self.book_id,
    #         'name': self.name,
    #         'description': self.description,
    #         'authors': [{'id': x.author_id, 'name': x.name} for x in self.authors],
    #         'rating': self.rating,
    #     }
    #     return data

    def delete(self):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_one_user(id):
        return Book.query.get(id)


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

    # def to_dict(self):
    #     data = {
    #         'author_id': self.author_id,
    #         'name': self.name,
    #         'sername': self.sername,
    #         'books': [
    #             {'id': x.book_id, 'name': x.name}
    #             for x
    #             in sorted(self.books, key=lambda x: x.rating, reverse=True)[:5]
    #         ]
    #     }
    #     return data

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_one_user(id):
        return Author.query.get(id)
