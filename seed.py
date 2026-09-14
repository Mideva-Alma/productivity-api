from app import app
from models import db, User, Note


with app.app_context():
    Note.query.delete()
    User.query.delete()

    user1 = User(username="john")
    user1.set_password("password123")

    user2 = User(username="jane")
    user2.set_password("password123")

    db.session.add_all([user1, user2])
    db.session.commit()

    note1 = Note(
        title="Welcome Note",
        content="Welcome to the productivity app!",
        user_id=user1.id
    )

    note2 = Note(
        title="Study Plan",
        content="Complete Flask authentication and CRUD.",
        user_id=user1.id
    )

    note3 = Note(
        title="Shopping List",
        content="Buy milk, bread, and fruits.",
        user_id=user2.id
    )

    db.session.add_all([note1, note2, note3])
    db.session.commit()

    print("Database seeded successfully!")