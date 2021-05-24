from datetime import datetime
from uuid import uuid4

from sqlalchemy import event
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from application.models import constants


class Webinar(db.Model):
    __tablename__ = constants.WEBINAR.TABLE_NAME
    # this will ensure no duplicate data in database
    __table_args__ = (
        db.UniqueConstraint(
            "title",
            "instructor_id",
            "subject_id",
            "course_id",
            name="uix_webinar_instructor_id_subject_id_course_id",
        ),
    )
    # identity fields
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # personal details
    title = db.Column(db.String)
    start_time = db.Column(db.TIMESTAMP, default=datetime.now())
    duration = db.Column(db.FLOAT)

    # relationship details
    instructor_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.USER.TABLE_NAME}.id", ondelete="CASCADE"),
    )
    instructor = db.relationship(constants.USER.OBJ_NAME, back_populates="webinars")

    course_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.COURSE.TABLE_NAME}.id", ondelete="CASCADE"),
    )
    subject_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.SUBJECT.TABLE_NAME}.id", ondelete="CASCADE"),
    )
    tag_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.TAG.TABLE_NAME}.id", ondelete="CASCADE"),
    )

    view_count = db.Column(db.Integer)


@event.listens_for(Webinar, "after_update")
def increase_course_view_count(mapper, connection, target: Webinar) -> None:
    Webinar.view_count = target.view_count + 1
