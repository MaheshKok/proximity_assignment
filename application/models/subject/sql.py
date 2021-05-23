from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from application.models import constants


class Subject(db.Model):
    __tablename__ = constants.SUBJECT.TABLE_NAME
    # this will ensure no duplicate subject shall exist in database
    __table_args__ = (
        db.UniqueConstraint("name", "instructor_id", name="uix_subject_per_instructor"),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String)

    instructor_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.USER.TABLE_NAME}.id", ondelete="CASCADE"),
    )
    instructor = db.relationship(constants.USER.OBJ_NAME, back_populates="subjects")

    tag_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.TAG.TABLE_NAME}.id", ondelete="CASCADE"),
    )

    webinars = db.relationship(constants.WEBINAR.OBJ_NAME, backref="subject")
    videos = db.relationship(constants.VIDEO.OBJ_NAME, backref="subject")
