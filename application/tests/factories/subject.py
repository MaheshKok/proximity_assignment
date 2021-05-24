import factory

from application.extensions import db
from application.models.subject.sql import Subject
from application.tests.factories.user import UserFactory


class SubjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Subject
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    title = factory.sequence(lambda n: f"test_subject_{n}")
    instructor = factory.SubFactory(UserFactory)
