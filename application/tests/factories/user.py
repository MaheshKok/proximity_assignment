import factory

from application.extensions import db
from application.models.user.sql import User
from application.tests.factories.course import CourseFactory
from application.tests.factories.subject import SubjectFactory
from application.tests.factories.tag import TagFactory
from application.tests.factories.video import VideoFactory
from application.tests.factories.webinar import WebinarFactory


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.sequence(lambda n: f"test_user_{n}")
    role = "instructor"

    course = factory.SubFactory(CourseFactory)
    Subject = factory.SubFactory(SubjectFactory)
    tag = factory.SubFactory(TagFactory)
    video = factory.SubFactory(VideoFactory)
    webinar = factory.SubFactory(WebinarFactory)

    view_count = 1