from flask import Blueprint
from flask import request
from flask import jsonify
from marshmallow.exceptions import ValidationError

from config import PAGINATE_VALUE
from models import Author, Book
from schemas import AuthorSchemaExt, AuthorAddBookSchema, BookDelAuthorSchema


authors = Blueprint('authors', __name__, url_prefix='/authors')

error_resp = {'success': False, 'message': '', 'validation_error': {}}
success_resp = {'success': True, 'message': ''}


@authors.route('', methods=['GET'])
def authors_get():
    author_id = request.args.get('id')
    author_schema = AuthorSchemaExt()

    if author_id is not None and author_id.isdigit():
        author = Author.get_one_item(author_id)
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
    e_response = error_resp
    s_response = success_resp

    try:
        a = author_schema.load(req_data)
    except ValidationError as e:
        e_response['validation_error'] = e.messages
        e_response['message'] = 'Validation error.'
        return jsonify(e_response)

    a.save()
    s_response['message'] = f'Author {a.name} was created.'
    return jsonify(s_response)


@authors.route('', methods=['PUT'])
def authors_put():
    """Добавить книгу к автору."""
    data = request.get_json()
    schema = AuthorAddBookSchema()
    e_response = error_resp
    s_response = success_resp

    try:
        a, books_id = schema.load(data)
        if a is None:
            e_response['message'] = f'Not found author with id={data["author_id"]}.'
            return jsonify(e_response)
    except ValidationError as e:
        e_response['validation_error'] = e.messages
        e_response['message'] = 'Validation error.'
        return jsonify(e_response)

    list_b = Book.query.filter(Book.book_id.in_(books_id))
    if list_b.count() <= 0:
        e_response['messages'] = f'Noone books found with id: {", ".join([str(x) for x in books_id])}.'
        return jsonify(e_response)

    found_books = []
    for b in list_b:
        found_books.append(b.book_id)
        a.books.append(b)
    a.save()
    s_response['message'] = f'Books was found with id: {", ".join([str(x) for x in found_books])}.'
    return jsonify(s_response)


@authors.route('', methods=['PATCH'])
def authors_patch():
    """Удалить связь книги к автором."""
    data = request.get_json()
    schema = BookDelAuthorSchema()
    e_response = error_resp
    s_response = success_resp

    try:
        b, a = schema.load(data)
    except ValidationError as e:
        e_response['validation_error'] = e.messages
        e_response['message'] = 'Validation error.'
        return jsonify(e_response)

    if a is None:
        e_response['message'] = f'Not found author with id={data["author_id"]}.'
        return jsonify(e_response)
    if b is None:
        e_response['message'] = f'Not found book with id={data["book_id"]}.'
        return jsonify(e_response)
    if len(b.authors) == 1:
        e_response['message'] = f'Book have only one author. Its impossible to delete last author.'
        return jsonify(e_response)

    try:
        a.books.remove(b)
    except ValueError:
        e_response['message'] = f'Author with id={data["author_id"]} isn\'t the author of book with id={data["book_id"]}.'
        return jsonify(e_response)

    s_response['message'] = f'Author with id={data["author_id"]} was removed from book.'
    a.save()
    return jsonify(s_response)
