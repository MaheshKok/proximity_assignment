from datetime import datetime

import factory

from application.extensions import db
from application.models.webinar.sql import Webinar
from application.tests.factories.user import UserFactory


class WebinarFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Webinar
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    title = factory.sequence(lambda n: f"test_webinar_{n}")
    start_time = datetime.now()
    duration = 60

    instructor = factory.SubFactory(UserFactory)

    view_count = 1
