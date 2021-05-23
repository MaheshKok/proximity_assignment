import factory

from application.extensions import db
from application.models.course.sql import Course
from application.tests.factories.tag import TagFactory
from application.tests.factories.user import UserFactory
from application.tests.factories.video import VideoFactory
from application.tests.factories.webinar import WebinarFactory


class CourseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Course
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.sequence(lambda n: f"test_course_{n}")
    instructor = factory.SubFactory(UserFactory)
    tag = factory.SubFactory(TagFactory)
    video = factory.SubFactory(VideoFactory)
    webinar = factory.SubFactory(WebinarFactory)

    view_count = 1
