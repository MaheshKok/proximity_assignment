from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from application.models import constants


class Tag(db.Model):
    __tablename__ = constants.TAG.TABLE_NAME
    # this will ensure no duplicate tag shall exist in database
    __table_args__ = (
        db.UniqueConstraint("title", "instructor_id", name="uix_tag_per_instructor"),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String, nullable=False)

    instructor_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.USER.TABLE_NAME}.id", ondelete="CASCADE"),
        nullable=False,
    )
    instructor = db.relationship(constants.USER.OBJ_NAME, back_populates="tags")
    courses = db.relationship(constants.COURSE.OBJ_NAME, backref="tag")
    subjects = db.relationship(constants.SUBJECT.OBJ_NAME, backref="tag")
    videos = db.relationship(constants.VIDEO.OBJ_NAME, backref="tag")
    webinars = db.relationship(constants.WEBINAR.OBJ_NAME, backref="tag")
