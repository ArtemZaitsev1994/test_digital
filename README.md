# Тестовое задание "Авторы и книги".

Два Docker-контейнера: сервер с API, база данных mysql.

## Логика работы
Для начала создается Автор книг, потом создаются книги. Книги не могут быть созданы без автора - автор может быть создан без книг.

## Техническое описание
Так как сервер подразумевается использовать совместно с SPA-приложением, то удобнее всего общаться с помощью JSON-формата. Сервер принимает запросы с JSON-данными и отвечает JSON-данными.
Сервер работает на Flask-фреймворке. В качестве базы данных выступает mysql.

Перменные окружения для приложения указаны в /server/.env файле.
* `DEBUG` - Включить\выключить debug-mode.
* `TESTING` - Режим тестирования.
* `CSRF_ENABLED` - Поддержка CSRF.
* `SECRET_KEY` - Секретный ключ.
* `SQLALCHEMY_DATABASE_URI` - Адрес базы.
* `SQLALCHEMY_TRACK_MODIFICATIONS` - Отслеживать изменения объектов в базе и посылать сигналы.
* `PAGINATE_VALUE` - Количество записей на странице.

## Запуск приложения
Для удобства приложение упаковано в Docker.
Клонируйте репозиторий.
> git clone https://github.com/ArtemZaitsev1994/test_digital.git

Перейдите в папку с проектом.
> cd test_digital

Запустите сборку Docker-compose
> sudo docker-compose build

> sudo docker-compose up

Приложение запускается не сразу, в особенности mysql - придется подождать. Сервер будет доступен по адресу `0.0.0.0:8080`

## API
### Создание автора:
#### Curl пример
```
curl --header "Content-Type: application/json" --request POST --data '{"name": "Artem", "sername": "Zaitsev"}' http://0.0.0.0:8080/authors
```
#### URL
`http://0.0.0.0:8080/authors`
#### Тип запроса
`POST`
#### JSON request data
```
{
  "name": str,
  "sername": str
}
```
* `name` - Имя автора.
* `sername` - Фамилия автора.

#### Success response
```
{
  'success': True,
  'message': str
}
```
* `message` - Сообщение о том, какой пользователь был создан.

#### Fail response
```
{
  'success': False,
  'message': str,
  'validation_error': dict[str, str]
}
```
* `message` - Сообщение ошибки.
* `validation_error` - Словарь ошибок.

#### Получение автора:
#### Curl пример
```
curl --header "Content-Type: application/json" --request GET http://0.0.0.0:8080/authors?id=1
```
#### URL
`http://0.0.0.0:8080/authors?id=1`
#### Тип запроса
`GET`
#### Параметры запроса
```
id - int
```
* `id` - ID автора.

#### Success response
```
{
  'author_id': int,
  'name': str,
  'sername': str,
  'books': [{
    'book_id': int,
    'name': str,
    'description': str,
    'rating': float,
    'count_marks': int,
  },]
}
```
* `author_id` - ID запрашиваемого автора.
* `name` - Имя автора.
* `sername` - Фамилия автора.
* `books` - Массив из словарей, содержащий книги.
* `books.book_id` - ID книги.
* `books.name` - Имя книги.
* `books.description` - Описание книги.
* `books.rating` - Текущий рейтинг.
* `books.count_marks` - Количество оценок книги.

#### Fail response
```
{
  'success': False,
  'message': str
}
```
* `message` - Сообщение об ошибке.


#### Получение списка авторов:
#### Curl пример
```
curl --header "Content-Type: application/json" --request GET http://0.0.0.0:8080/authors?page=1&pagin=10
```
#### URL
`http://0.0.0.0:8080/authors?page=1&pagin=3`
#### Тип запроса
`GET`
#### Параметры запроса
```
page - int
pagin - int
```
* `page` - номер страницы.
* `pagin` - количество авторов на странице, по умолчанию 3.

#### Success response
```
{
  'authors': [{
    'author_id': int,
    'name': str,
    'sername': str,
    'books': [{
      'book_id': int,
      'name': str,
      'description': str,
      'rating': float,
      'count_marks': int,
    },]
  }],
  'pagination': {
    'has_next': bool,
    'has_prev': bool,
    'next_num': int or null,
    'prev_num': int or null,
    'pages': int
  }
}
```
* `authors` - Список авторов.
* `authors.author_id` - ID автора.
* `authors.name` - Имя автора.
* `authors.sername` - Фамилия автора.
* `authors.books` - Массив из словарей, содержащий книги (5 топовых).
* `authors.books.book_id` - ID книги.
* `authors.books.name` - Имя книги.
* `authors.books.description` - Описание книги.
* `authors.books.rating` - Текущий рейтинг.
* `pagination.has_next` - Наличие следующей страницы.
* `pagination.has_prev` - Наличие предыдущей страницы.
* `pagination.next_num` - Номер следующей страницы.
* `pagination.prev_num` - Номер предыдущей страницы.
* `pagination.pages` - Всего количество страниц.

### Создание книги:
#### Curl пример
```
curl --header "Content-Type: application/json" --request POST --data '{"book": {"name": "Kolobok", "description": "The story about bread."}, "author_id": [1, 2]}' http://0.0.0.0:8080/books
```
#### URL
`http://0.0.0.0:8080/books`
#### Тип запроса
`POST`
#### JSON request data
```
{
  "name": str,
  "description": str
  "authors": list[int, ]
}
```
* `name` - Название книги.
* `description` - Описание книги.
* `authors` - Массив авторов.

#### Success response
```
{
  'success': True,
  'message': str
}
```
* `message` - Сообщение о том, какие авторы были найдены и к которым была добавлена книга.

#### Fail response
```
{
  'success': False,
  'message': str,
  'validation_error': dict[str, str]
}
```
* `message` - Сообщение ошибки.
* `validation_error` - Словарь ошибок.

### Добавление книги к автору:
#### Curl пример
```
curl --header "Content-Type: application/json" --data '{"author_id": 1, "book_id": [2, 3]}' --request PUT http://0.0.0.0:8080/authors
```
#### URL
`http://0.0.0.0:8080/authors`
#### Тип запроса
`PUT`
#### JSON request data
```
{
  "author_id": int,
  "book_id": [int, ]
}
```
* `author_id` - ID автора.
* `book_id` - Список ID книг.

#### Success response
```
{
  'success': True,
  'message': str,
}
```
* `message` - Сообщение о том, какие книги были добавлены.

#### Fail response
```
{
  'success': False,
  'message': str,
  'validation_error': dict[str, str]
}
```
* `message` - Сообщение ошибки.
* `validation_error` - Словарь ошибок.

### Добавление автора к книге:
#### Curl пример
```
curl --header "Content-Type: application/json" --data '{"book_id": 22, "author_id": [18]}' --request PUT http://0.0.0.0:8080/books
```
#### URL
`http://0.0.0.0:8080/books`
#### Тип запроса
`PUT`
#### JSON request data
```
{
  "book_id": int,
  "author_id": list[int, ]
}
```
* `book_id` - ID книги.
* `author_id` - Массив авторов.

#### Success response
```
{
  'success': True,
  'message': str,
}
```
* `message` - Сообщение о том, какие авторы были найдены и к которым была добавлена книга.

#### Fail response
```
{
  'success': False,
  'message': str,
  'validation_error': dict[str, str]
}
```
* `message` - Сообщение ошибки.
* `validation_error` - Словарь ошибок.

### Убрать связь между книгой и автором:
#### Curl пример
```
curl --header "Content-Type: application/json" --data '{"book_id": 1, "author_id": 1}' --request PATCH http://0.0.0.0:8080/authors
```
#### URL
`http://0.0.0.0:8080/authors`
#### Тип запроса
`PATCH`
#### JSON request data
```
{
  "book_id": int,
  "author_id": int
}
```
* `book_id` - ID книги.
* `author_id` - ID автора.

#### Success response
```
{
  'success': True,
  'message': str,
}
```
* `message` - Сообщение.

#### Fail response
```
{
  'success': False,
  'message': str,
  'validation_error': dict[str, str]
}
```
* `message` - Сообщение ошибки.
* `validation_error` - Словарь ошибок.

#### Получение книги:
#### Curl пример
```
curl --header "Content-Type: application/json" --request GET http://0.0.0.0:8080/books?id=1
```
#### URL
`http://0.0.0.0:8080/books?id=1`
#### Тип запроса
`GET`
#### Параметры запроса
```
id - int
```
* `id` - ID книги.

#### Success response
```
{
  'book_id': int,
  'name': str,
  'description': str,
  'rating': float,
  'count_marks': int,
  'authors': [{
    'author_id': int,
    'name': str,
    'sername': str,
  },]
}
```
* `book_id` - ID книги.
* `name` - Имя книги.
* `description` - Описание книги.
* `rating` - Текущий рейтинг.
* `count_marks` - Количество оценок книги.
* `authors` - Массив из авторов книги.
* `authors.author_id` - ID автора.
* `authors.name` - Имя автора.
* `authors.sername` - Фамилия автора.

#### Fail response
```
{
  'success': False,
  'message': str,
}
```
* `message` - Сообщение об ошибке.

#### Получение списка книг:
#### Curl пример
```
curl --request GET http://0.0.0.0:8080/books?page=1&pagin=10
```
#### URL
`http://0.0.0.0:8080/books?page=1&pagin=10`
#### Тип запроса
`GET`
#### Параметры запроса
```
page - int
pagin - int
```
* `page` - номер страницы.
* `id` - количество авторов на странице, по умолчанию 3.

#### Success response
```
{
  'books': [{
    'book_id': int,
    'name': str,
    'description': str,
    'rating': float,
    'count_marks': int,
    'authors': [{
      'author_id': int,
      'name': str,
      'sername': str,
    },]
  }],
  'pagination': {
    'has_next': bool,
    'has_prev': bool,
    'next_num': int or null,
    'prev_num': int or null,
    'pages': int
  }
}
```
* `books.book_id` - ID книги.
* `books.name` - Имя книги.
* `books.description` - Описание книги.
* `books.rating` - Текущий рейтинг.
* `books.count_marks` - Количество оценок книги.
* `books.authors` - Массив из авторов книги.
* `books.authors.author_id` - ID автора.
* `books.authors.name` - Имя автора.
* `books.authors.sername` - Фамилия автора.
* `pagination.has_next` - Наличие следующей страницы.
* `pagination.has_prev` - Наличие предыдущей страницы.
* `pagination.next_num` - Номер следующей страницы.
* `pagination.prev_num` - Номер предыдущей страницы.
* `pagination.pages` - Всего количество страниц.

### Добавление оценки к книге:
#### Curl пример
```
curl --header "Content-Type: application/json" --data '{"book_id": 1, "rating": 5}' --request PATCH http://0.0.0.0:8080/books
```
#### URL
`http://0.0.0.0:8080/books`
#### Тип запроса
`PATCH`
#### JSON request data
```
{
  "book_id": int,
  "rating": int
}
```
* `book_id` - ID книги.
* `rating` - Оценка книги (целове число от 1 до 5).

#### Success response
```
{
  'success': True,
  'message': str,
  'rating': float,
  'votes': int
}
```
* `message` - Сообщение о том, какие авторы были найдены и к которым была добавлена книга.
* `rating` - Текущий рейтинг.
* `votes` - Количество голосов.

#### Fail response
```
{
  'success': False,
  'message': str,
  'validation_error': dict[str, str]
}
```
* `message` - Сообщение ошибки.
* `validation_error` - Словарь ошибок.

## Тесты
Для приложения подготовлены небольшие тесты. Тесты следует запускать при развернутой в Docker базе данных, дабы избежать потери данных. В файле data_test.py содержатся данные для тестов, в test.py - сами тесты.

Разоваричаем проект:
> sudo docker-compose up --build -d

Останавливаем сервер:
> sudo docker stop server

Разворачиваем виртуальное окружение:
> python3 -m venv env

Активируем виртуальное окружение:
> source env/bin/activate

Переходим в папку с тестами:
> cd server

Запускаем тесты:
> python test.py

Второй вариант - запуск тестов внутри контейнера.
