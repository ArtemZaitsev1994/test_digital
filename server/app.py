from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object('config.Config')



# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

ma = Marshmallow(app)

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('~~*!pong!*~~')

if __name__ == '__main__':
    from authors.blueprint import authors
    from books.blueprint import books
    from models import Book
    from models import Author

    app.register_blueprint(authors)
    app.register_blueprint(books)
    app.run(debug=True)
