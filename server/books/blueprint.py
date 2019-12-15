from flask import Blueprint
from flask import request
from flask import jsonify
from marshmallow.exceptions import ValidationError

from config import PAGINATE_VALUE
from models import Author, Book
from schemas import BookSchemaExt, AuthorIdList, BookRatingSchema, BookAddAuthorSchema
from app import db


books = Blueprint('books', __name__, url_prefix='/books')

error_resp = {'success': False, 'message': ''}
success_resp = {'success': True, 'message': ''}


@books.route('', methods=['GET'])
def books_get():
    book_id = request.args.get('id')
    book_schema = BookSchemaExt()

    if book_id is not None and book_id.isdigit():
        book = Book.query.get_or_404(book_id)
        response = book_schema.dump(book)
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
        data = book_schema.dump(books.items, many=True)
        response = {
            'books': data,
            'pagination': {
                'has_next': books.has_next,
                'has_prev': books.has_prev,
                'next_num': books.next_num,
                'prev_num': books.prev_num,
                'pages': books.pages
            }
        }
    return jsonify(response)


@books.route('', methods=['POST', 'PUT'])
def books_post():
    data = request.get_json()

    if request.method == 'POST':
        book_schema = BookSchemaExt()
        schema = AuthorIdList()

        try:
            b = book_schema.load(data['book'])
        except ValidationError as e:
            error_resp['message'] = e.messages
            return jsonify(error_resp)

        try:
            author_id = schema.load({'author_id': data['author_id']})
        except ValidationError as e:
            error_resp['message'] = e.messages
            return jsonify(error_resp)


    elif request.method == 'PUT':
        schema = BookAddAuthorSchema()
        try:
            b, author_id = schema.load(data)
        except ValidationError as e:
            error_resp['message'] = e.messages
            return jsonify(error_resp)


    list_a = Author.query.filter(Author.author_id.in_(author_id))
    if list_a.count() <= 0:
        error_resp['messages'] = f'Noone authors found with id: {", ".join([str(x) for x in author_id])}.'
        return jsonify(error_resp)
    found_authors = []
    for a in list_a:
        found_authors.append(a.author_id)
        a.books.append(b)
    b.save()
    success_resp['message'] = f'Found authors: {", ".join([str(x) for x in found_authors])}.'
    return jsonify(success_resp)


@books.route('', methods=['PATCH'])
def books_patch():
    data = request.get_json()
    schema = BookRatingSchema()
   
    try:
        b, rating = schema.load(data)
    except ValidationError as e:
        error_resp['message'] = e.messages
        return jsonify(error_resp)

    if b is None:
        error_resp['message'] = f'No book found with id={data["book_id"]}'
        return jsonify(error_resp)

    b.count_marks += 1
    b.rating = (b.rating * (b.count_marks - 1) + rating) / b.count_marks
    b.save()
    success_resp['message'] = f'New rating {b.rating} for {b.count_marks} votes.'
    success_resp['rating'] = b.rating
    success_resp['votes'] = b.count_marks
    return jsonify(success_resp)
 

@books.route('', methods=['DELETE'])
def books_delete():
    pass
