import factory

from application.extensions import db
from application.models.video.sql import Video
from application.tests.factories.user import UserFactory


class VideoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Video
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    title = factory.sequence(lambda n: f"test_video_{n}")
    instructor = factory.SubFactory(UserFactory)

    view_count = 1
