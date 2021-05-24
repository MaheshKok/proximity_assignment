import factory

from application.extensions import db
from application.models.course.sql import Course
from application.tests.factories.user import UserFactory


class CourseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Course
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    title = factory.sequence(lambda n: f"test_course_{n}")
    instructor = factory.SubFactory(UserFactory)

    view_count = 1
