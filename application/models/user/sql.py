from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from application.models import constants


class User(db.Model):
    __tablename__ = constants.USER.TABLE_NAME

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    courses = db.relationship(
        constants.COURSE.OBJ_NAME,
        back_populates="instructor",
        cascade="save-update, all, delete-orphan",
    )
    subjects = db.relationship(
        constants.SUBJECT.OBJ_NAME,
        back_populates="instructor",
        cascade="save-update, all, delete-orphan",
    )
    tags = db.relationship(
        constants.TAG.OBJ_NAME,
        back_populates="instructor",
        cascade="save-update, all, delete-orphan",
    )
    videos = db.relationship(
        constants.VIDEO.OBJ_NAME,
        back_populates="instructor",
        cascade="save-update, all, delete-orphan",
    )
    webinars = db.relationship(
        constants.WEBINAR.OBJ_NAME,
        back_populates="instructor",
        cascade="save-update, all, delete-orphan",
    )
