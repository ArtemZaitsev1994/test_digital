# Тестовое задание "Авторы и книги".

Два Docker-контейнера: сервер с API, база данных mysql.

## Логика работы
Сервер принимает запросы с JSON-данными и отвечает JSON-данными.
Для начала создается Автор книг, потом создаются книги. Книги не могут быть созданы без автора - автор может быть создан без книг.

## Техническое описание
Сервер работает на Flask-фреймворке. В качестве базы данных выступает mysql.

Перменные окружения для приложения указаны в /server/.env файле.
* `MONGO_HOST` - Хост базы данных MongoDB
* `MONGO_DB_NAME` - Имя рабочей базы данных
* `RETRIES_TIMES` - Количество повторов при неудачной отправке сообщений
* `MESSENGER_HOST` - Хост сервера с мессенджерами
* `REDIS_HOST` - Адрес Redis-server
* `WAIT_BETWEEN_REQUESTS` - Время между попытками отправить запрос (секунд)

## Запуск приложения
Для удобства приложение упаковано в Docker.
Клонируйте репозиторий.
> git clone https://github.com/ArtemZaitsev1994/test_digital.git

Перейдите в папку с проектом.
> cd test_digital

Запустите сборку Docker-compose
> sudo docker-compose up --build -d

Сервер будет доступен по `localhost:8080`

## API
### Создание автора:
#### Curl пример
```
curl --header "Content-Type: application/json" --request POST --data '{"name": "Artem", "sername": "Zaitsev"}' http://localhost:5000/authors
```
#### URL
`http://localhost:8080/api/contacts`
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
  'message': 'Author <name> was created.'
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
curl --header "Content-Type: application/json" --request GET http://localhost:5000/authors?id=1
```
#### URL
`http://localhost:5000/authors?id=1`
#### Тип запроса
`GET`
#### JSON request data
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
  'message': 'No book found with id=<id>'
}
```
* `message` - Сообщение об ошибке.


#### Получение списка авторов:
#### Curl пример
```
curl --header "Content-Type: application/json" --request GET http://localhost:5000/authors?page=1&pagin=10
```
#### URL
`http://localhost:5000/authors?page=1&pagin=3`
#### Тип запроса
`GET`
#### JSON request data
```
page - int
pagin - int
```
* `page` - номер страницы.
* `id` - количество авторов на странице, по умолчанию 3.

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

### Добавление книги к автору:
#### Curl пример
```
curl --header "Content-Type: application/json" --data '{"author_id": 1, "book_id": [2, 3]}' --request PUT http://localhost:5000/authors
```
#### URL
`http://localhost:8080/authors`
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
* `book_id` - ID книги.

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

### Создание книги:
#### Curl пример
```
curl --header "Content-Type: application/json" --request POST --data '{"name": "Book name", "description": "Lorem ipsum dolor sit amet, consectetuer adipiscing", "authors": [1, 2]}' http://localhost:5000/books
```
#### URL
`http://localhost:8080/books`
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

### Добавление автора к книге:
#### Curl пример
```
curl --header "Content-Type: application/json" --data '{"book_id": 22, "author_id": [18]}' --request PUT http://localhost:5000/books```
#### URL
`http://localhost:8080/books`
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



#### Получение книги:
#### Curl пример
```
curl --header "Content-Type: application/json" --request GET http://localhost:5000/books?id=1
```
#### URL
`http://localhost:5000/books?id=1`
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
curl --request GET http://localhost:5000/books?page=1&pagin=10
```
#### URL
`http://localhost:5000/books?page=1&pagin=10`
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
curl --header "Content-Type: application/json" --data '{"book_id": 1, "rating": 5}' --request PATCH http://localhost:5000/books```
#### URL
`http://localhost:8080/books`
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
* `rating` - Оценка книги.

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








### Отправка сообщений:
#### Curl пример
```
curl --header "Content-Type: application/json" --request PUT --data '{"user_name": "test", "contacts": ["Artem", "Lera", "Vasya"], "message": "Hello there", "time": [2019, 11, 30, 14, 0, 6]}' http://localhost:8080/api/contacts
```
#### URL
`http://localhost:8080/api/contacts`
#### JSON request data
```
{
  'user_name': str,
  'contacts': list[name: str, ...],
  'message': str,
  'time': list[int, int, int, int, int, int],
}
```
* `user_name` - Имя, под которым выполняется запрос.
* `contact` - список имён контактов, кому хотим отправить сообщение.
* `message` - текст сообщения.
* `time` - время, не раньше которого нужно начать отправку (текущее или раньше, чтобы отправить при получении).

#### Response
```
{
  'success': bool,
  'wrong_contacts': [{
    'name': str,
    'error': str,
  }, ...]
}
```
* `success` - булево значение, возвращает True, только если сообщения удачно разосланы всем контактам.
* `wrong_contacts` - список контактов, кому не удалось разослать сообщения.
* `wrong_contacts.name` - имя контакта.
* `wrong_contacts.error` - текст ошибки.

### Получить список своих контактов:
#### Curl пример
```
curl --header "Content-Type: application/json" --request GET --data '{"user_name": "test"}' http://localhost:8080/api/contacts
```
#### URL
`http://localhost:8080/api/contacts`
#### JSON request data
```
{
  'user_name': str,
}
```
* `user_name` - Имя, под которым выполняется запрос.
#### Response
```
{
  'contacts': {
    name: {
      'telegram': str,
      'whatsApp': str,
      'viber': str,
    },
  }
}
```
* `contacts` - словарь контактов, ключами в котором являются имена контактов.
* `contacts[name].telegram` - идентификатор в Telegram.
* `contacts[name].whatsApp` - идентификатор в WhatsApp.
* `contacts[name].viber` - идентификатор в Viber.

### Получить недоставленные сообщения:
#### Curl пример
```
curl --header "Content-Type: application/json" --request GET --data '{"user_name": "test"}' http://localhost:8080/api/get_failed_mess
```
#### URL
`http://localhost:8080/api/get_failed_mess`
#### JSON request data
```
{
  'user_name': str,
}
```
* `user_name` - Имя, под которым выполняется запрос.
#### Response
```
{
  'data': {
    'sender': 'test',
    'message': 'f',
    'contact': 'asd',
    'url': 'http://0.0.0.0:8081/viber',
    'time': [2019, 11, 30, 13, 19, 18]
  }
}
```
* `data.sender` - юзер из под которого было создано сообщение.
* `data.message` - текст сообщения.
* `data.contact` - имя контакта, которому было адресовано сообщение.
* `data.url` - адрес сервиса, на который была попытка отправить.
* `data.time` - время, на которое было назначена отправка.

## Тесты
Для приложения подготовлены небольшие тесты. Тесты следует запускать при развернутом в Docker приложении, чтобы работа проводилась с развернутыми базами данных в контейнерах, дабы избежать потери данных.

Разоваричаем проект:
> sudo docker-compose up --build -d

Останавливаем сервер:
> sudo docker server stop

Переходим в папку с тестами:
> cd server