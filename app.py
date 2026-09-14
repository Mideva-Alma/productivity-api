from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from models import db, bcrypt, User, Note
from schemas import UserSchema, NoteSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///productivity.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

user_schema = UserSchema()
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


@app.route("/")
def home():
    return {"message": "Productivity API is running"}


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    try:
        validated_data = user_schema.load(data)
    except Exception as error:
        return {"errors": error.messages}, 400

    if User.query.filter_by(username=validated_data["username"]).first():
        return {"error": "Username already exists"}, 409

    user = User(username=validated_data["username"])
    user.set_password(validated_data["password"])

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.check_password(data.get("password", "")):
        return {"error": "Invalid username or password"}, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 200


@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "username": user.username
    }, 200

@app.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 5

    pagination = Note.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "notes": notes_schema.dump(pagination.items),
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }, 200


@app.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    try:
        validated_data = note_schema.load(data)
    except Exception as error:
        return {"errors": error.messages}, 400

    note = Note(
        title=validated_data["title"],
        content=validated_data["content"],
        user_id=user_id
    )

    db.session.add(note)
    db.session.commit()

    return note_schema.dump(note), 201


@app.route("/notes/<int:note_id>", methods=["PATCH"])
@jwt_required()
def update_note(note_id):
    user_id = int(get_jwt_identity())

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        return {"error": "Note not found"}, 404

    data = request.get_json()

    try:
        validated_data = note_schema.load(data, partial=True)
    except Exception as error:
        return {"errors": error.messages}, 400

    if "title" in validated_data:
        note.title = validated_data["title"]

    if "content" in validated_data:
        note.content = validated_data["content"]

    db.session.commit()

    return note_schema.dump(note), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    user_id = int(get_jwt_identity())

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        return {"error": "Note not found"}, 404

    db.session.delete(note)
    db.session.commit()

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)