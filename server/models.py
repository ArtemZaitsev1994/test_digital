from app import db


# Таблица для связи МногиеКоМногим авторов и книг
books = db.Table('books',
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id'), primary_key=True)
)


class Book(db.Model):
    """Описание модели книг"""
    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    rating = db.Column(db.Float(), default=.0)
    count_marks = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Book {self.name}>'

    def delete(self):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_one_user(id):
        return Book.query.get(id)


class Author(db.Model):
    """Описание модели автор"""
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    sername = db.Column(db.String(80), unique=False, nullable=True)

    books = db.relationship('Book', secondary=books, lazy='subquery',
        backref=db.backref('authors', lazy=True))

    def __init__(self, **kwargs):
        super(Author, self).__init__(**kwargs)
    
    def __repr__(self):
        return f'<Author {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_one_user(id):
        return Author.query.get(id)
