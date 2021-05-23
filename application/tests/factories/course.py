import factory

from application.extensions import db

from application.tests.factories import  TagFactory, VideoFactory, WebinarFactory
from application.tests.factories import UserFactory


class CourseFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        from application.models.course.sql import Course
        model = Course
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.sequence(lambda n: f"test_course_{n}")
    instructor = factory.SubFactory(UserFactory)
    tag = factory.SubFactory(TagFactory)
    video = factory.SubFactory(VideoFactory)
    webinar = factory.SubFactory(WebinarFactory)

    view_count = 1
