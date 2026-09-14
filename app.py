from flask import Flask
from flask_migrate import Migrate
from models import db, bcrypt, User, Note

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///productivity.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return {"message": "Productivity API is running"}


if __name__ == "__main__":
    app.run(debug=True)
