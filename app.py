from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from models import db, bcrypt, User, Note
from schemas import UserSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///productivity.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

user_schema = UserSchema()


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


if __name__ == "__main__":
    app.run(debug=True)