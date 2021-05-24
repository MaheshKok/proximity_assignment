from uuid import uuid4

from sqlalchemy import event
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from application.models import constants


class Course(db.Model):

    __tablename__ = constants.COURSE.TABLE_NAME
    # this will ensure no duplicate courses shall exist in database
    __table_args__ = (
        db.UniqueConstraint("title", "instructor_id", name="uix_course_per_instructor"),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String, nullable=False)

    instructor_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.USER.TABLE_NAME}.id", ondelete="CASCADE"),
        nullable=False,
    )
    instructor = db.relationship(constants.USER.OBJ_NAME, back_populates="courses")

    tag_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.TAG.TABLE_NAME}.id", ondelete="CASCADE"),
        nullable=True,
    )

    webinars = db.relationship(constants.WEBINAR.OBJ_NAME, backref="course")
    videos = db.relationship(constants.VIDEO.OBJ_NAME, backref="course")
    view_count = db.Column(db.Integer, default=1)


@event.listens_for(Course, "after_update")
def increase_course_view_count(mapper, connection, target: Course) -> None:
    Course.view_count = target.view_count + 1
