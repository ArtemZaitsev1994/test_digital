from flask import Flask, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

ma = Marshmallow(app)

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('~~*!pong!*~~')

if __name__ == '__main__':
    from authors.blueprint import authors
    from books.blueprint import books as blueprint_books
    from models import *
    db.create_all()

    app.register_blueprint(authors)
    app.register_blueprint(blueprint_books)
    app.run(debug=True, port=8080, host='0.0.0.0')
