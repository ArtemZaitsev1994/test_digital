from marshmallow import fields, Schema, post_load, validate

from models import Author, Book


class BookSchema(Schema):
    """Основаня схема книги"""
    book_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    rating = fields.Int()
    count_marks = fields.Int()


class AuthorSchema(Schema):
    """Основаня схема автора"""
    author_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    sername = fields.Str(required=True)


class BookSchemaExt(BookSchema):
    """Расширение схемы книги полем 'автор'."""
    authors = fields.Nested(AuthorSchema, many=True)

    @post_load
    def make_author(self, data, **kwargs):
        return Book(**data)


class AuthorSchemaExt(AuthorSchema):
    """Расширение схемы автора полем 'книги'."""
    books = fields.Nested(BookSchema, many=True)

    @post_load
    def make_author(self, data, **kwargs):
        return Author(**data)


class AuthorAddBookSchema(Schema):
    author_id = fields.Int(required=True)
    book_id = fields.List(fields.Int)

    @post_load
    def make_author(self, data, **kwargs):
        a = Author.get_one_user(data['author_id'])
        return a, data['book_id']


class BookAddAuthorSchema(Schema):
    book_id = fields.Int(required=True)
    author_id = fields.List(fields.Int)

    @post_load
    def make_author(self, data, **kwargs):
        b = Book.get_one_user(data['book_id'])
        return b, data['author_id']


class AuthorIdList(Schema):
    """Схема для валидации ID авторов."""
    author_id = fields.List(
        fields.Int,
        required=True,
        validate=[validate.Length(min=1)]
    )

    @post_load
    def make_author(self, data, **kwargs):
        return data['author_id']


class BookRatingSchema(Schema):
    """Схема для валидации изменения рейтинга книги."""
    book_id = fields.Int(required=True)
    rating = fields.Int(
        required=True, 
        validate=[validate.Range(0, 5)]
    )

    @post_load
    def make_author(self, data, **kwargs):
        b = Book.get_one_user(data['book_id'])
        return b, data['rating']
