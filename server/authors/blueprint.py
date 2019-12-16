from flask import Blueprint
from flask import request
from flask import jsonify
from marshmallow.exceptions import ValidationError

from config import PAGINATE_VALUE
from models import Author, Book
from schemas import AuthorSchemaExt, AuthorAddBookSchema


authors = Blueprint('authors', __name__, url_prefix='/authors')

error_resp = {'success': False, 'message': '', 'validation_error': {}}
success_resp = {'success': True, 'message': ''}


@authors.route('', methods=['GET'])
def authors_get():
    author_id = request.args.get('id')
    author_schema = AuthorSchemaExt()

    if author_id is not None and author_id.isdigit():
        author = Author.get_one_user(author_id)
        if author is None:
            response = success_resp
            response['message'] = f'No book found with id={author_id}'
            return jsonify(response)
        response = author_schema.dump(author)
    else:
        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        pagin = request.args.get('pagin')
        if pagin and pagin.isdigit():
            pagin = int(page)
        else:
            pagin = PAGINATE_VALUE

        authors = Author.query.filter().paginate(
            page=page,
            per_page=pagin
        )
        data = author_schema.dump(authors.items, many=True)
        for a in data:
            a['books'] = [x for x in sorted(a['books'], key=lambda y: y['rating'], reverse=True)[:5]]

        response = {
            'authors': data,
            'pagination': {
                'has_next': authors.has_next,
                'has_prev': authors.has_prev,
                'next_num': authors.next_num,
                'prev_num': authors.prev_num,
                'pages': authors.pages
            }
        }
    return jsonify(response)


@authors.route('', methods=['POST'])
def authors_post():
    """Создание автора."""
    req_data = request.get_json()
    author_schema = AuthorSchemaExt()

    try:
        a = author_schema.load(req_data)
    except ValidationError as e:
        error_resp['validation_error'] = e.messages
        error_resp['message'] = 'Validation error.'
        return jsonify(error_resp)

    a.save()
    success_resp['message'] = f'Author {a.name} was created.'
    return jsonify(success_resp)


@authors.route('', methods=['PUT'])
def authors_put():
    """Добавить книгу к автору."""
    data = request.get_json()
    schema = AuthorAddBookSchema()

    try:
        a, books_id = schema.load(data)
    except ValidationError as e:
        error_resp['validation_error'] = e.messages
        error_resp['message'] = 'Validation error.'
        return jsonify(error_resp)

    list_b = Book.query.filter(Book.book_id.in_(books_id))
    if list_b.count() <= 0:
        error_resp['messages'] = f'Noone books found with id: {", ".join([str(x) for x in books_id])}.'
        return jsonify(error_resp)

    found_books = []
    for b in list_b:
        found_books.append(b.book_id)
        a.books.append(b)
    a.save()
    success_resp['message'] = f'Books was found with id: {", ".join([str(x) for x in found_books])}.'
    return jsonify(success_resp)
