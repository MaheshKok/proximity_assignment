from datetime import datetime

import factory

from application.extensions import db
from application.models.webinar.sql import Webinar
from application.tests.factories.tag import TagFactory
from application.tests.factories.user import UserFactory


class WebinarFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Webinar
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.sequence(lambda n: f"test_webinar_{n}")
    start_time = datetime.now()
    duration = 60

    tag = factory.SubFactory(TagFactory)
    instructor = factory.SubFactory(UserFactory)
