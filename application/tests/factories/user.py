from datetime import datetime

import factory
from application.models.user.sql import User
from application.extensions import db


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.sequence(lambda n: f"test_user_{n}")
    role = "instructor"
