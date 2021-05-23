import factory

from application.extensions import db
from application.models.subject.sql import Subject
from application.tests.factories.tag import TagFactory
from application.tests.factories.user import UserFactory
from application.tests.factories.video import VideoFactory
from application.tests.factories.webinar import WebinarFactory


class SubjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Subject
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.sequence(lambda n: f"test_subject_{n}")
    instructor = factory.SubFactory(UserFactory)

    tag = factory.SubFactory(TagFactory)
    video = factory.SubFactory(VideoFactory)
    webinar = factory.SubFactory(WebinarFactory)

    view_count = 1