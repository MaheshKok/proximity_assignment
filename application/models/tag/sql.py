from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from application.extensions import db
from application.models import constants


class Tag(db.Model):
    __tablename__ = constants.TAG.TABLE_NAME

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String)

    instructor_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f"{constants.USER.TABLE_NAME}.id", ondelete="CASCADE"))
    instructor = db.relationship(
        constants.USER.OBJ_NAME, back_populates="tags"
    )
    courses = db.relationship(
        constants.COURSE.OBJ_NAME, backref="tag"
    )
    subjects = db.relationship(
        constants.SUBJECT.OBJ_NAME, backref="tag"
    )
    videos = db.relationship(
        constants.VIDEO.OBJ_NAME, backref="tag"
    )
    webinars = db.relationship(
        constants.WEBINAR.OBJ_NAME, backref="tag"
    )

