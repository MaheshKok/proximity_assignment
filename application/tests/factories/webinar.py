from datetime import datetime

import factory

from application.extensions import db
from application.tests.factories.tag import TagFactory


class WebinarFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        from application.models.webinar.sql import Webinar
        model = Webinar
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.sequence(lambda n: f"test_webinar_{n}")
    start_time = datetime.now()
    duration = 60

    tag = factory.SubFactory(TagFactory)
    instructor = factory.SubFactory(UserFactory)

    view_count = 1
