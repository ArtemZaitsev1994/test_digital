from flask import Blueprint
from flask import request
from flask import jsonify
from marshmallow.exceptions import ValidationError

from config import PAGINATE_VALUE
from models import Author, Book
from schemas import BookSchemaExt, AuthorIdList, BookRatingSchema, BookAddAuthorSchema


books = Blueprint('books', __name__, url_prefix='/books')

error_resp = {'success': False, 'message': '', 'validation_error': {}}
success_resp = {'success': True, 'message': ''}


@books.route('', methods=['GET'])
def books_get():
    """Получение книг"""
    book_id = request.args.get('id')
    book_schema = BookSchemaExt()

    if book_id is not None and book_id.isdigit():
        # Получить книгу по ID
        book = Book.get_one_item(book_id)
        if book is None:
            response = success_resp
            response['message'] = f'No book found with id={book_id}'
            return jsonify(response)
        response = book_schema.dump(book)
    else:
        # Получить все книги
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

        books = Book.query.filter().paginate(
            page=page,
            per_page=pagin
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
    """Создание/изменение книги книги"""
    data = request.get_json()
    e_response = error_resp
    s_response = success_resp

    if request.method == 'POST':
        """Создание книги"""
        book_schema = BookSchemaExt()
        schema = AuthorIdList()

        try:
            b = book_schema.load(data['book'])
        except ValidationError as e:
            e_response['validation_error'] = e.messages
            e_response['message'] = 'Validation error.'
            return jsonify(e_response)

        try:
            author_id = schema.load({'author_id': data['author_id']})
        except ValidationError as e:
            e_response['validation_error'] = e.messages
            e_response['message'] = 'Validation error.'
            return jsonify(e_response)


    elif request.method == 'PUT':
        """Добавление авторов книги"""
        schema = BookAddAuthorSchema()
        try:
            b, author_id = schema.load(data)
        except ValidationError as e:
            e_response['validation_error'] = e.messages
            e_response['message'] = 'Validation error.'
            return jsonify(e_response)


    list_a = Author.query.filter(Author.author_id.in_(author_id))
    if list_a.count() <= 0:
        e_response['messages'] = f'Noone authors found with id: {", ".join([str(x) for x in author_id])}.'
        return jsonify(e_response)
    found_authors = []
    for a in list_a:
        found_authors.append(a.author_id)
        a.books.append(b)
    b.save()
    s_response['message'] = f'Found authors: {", ".join([str(x) for x in found_authors])}.'
    return jsonify(s_response)


@books.route('', methods=['PATCH'])
def books_patch():
    """Добавление оценки к книге"""
    data = request.get_json()
    schema = BookRatingSchema()
    e_response = error_resp
    s_response = success_resp
   
    try:
        b, rating = schema.load(data)
    except ValidationError as e:
        e_response['validation_error'] = e.messages
        e_response['message'] = 'Validation error.'
        return jsonify(e_response)

    if b is None:
        e_response['message'] = f'No book found with id={data["book_id"]}'
        return jsonify(e_response)

    b.count_marks += 1
    b.rating = (b.rating * (b.count_marks - 1) + rating) / b.count_marks
    b.save()
    s_response['message'] = f'New rating {b.rating} for {b.count_marks} votes.'
    s_response['rating'] = b.rating
    s_response['votes'] = b.count_marks
    return jsonify(s_response)
