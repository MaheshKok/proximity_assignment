import factory

from application.extensions import db
from application.models.user.sql import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    title = factory.sequence(lambda n: f"test_user_{n}")
    role = "instructor"
