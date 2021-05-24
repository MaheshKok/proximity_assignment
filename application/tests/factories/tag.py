import factory

from application.extensions import db
from application.models.tag.sql import Tag
from application.tests.factories.user import UserFactory


class TagFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Tag
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    title = factory.sequence(lambda n: f"test_tag_{n}")
    instructor = factory.SubFactory(UserFactory)
