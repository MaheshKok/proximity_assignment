from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from application.extensions import db
from application.models import constants


class Webinar(db.Model):
    __tablename__ = constants.WEBINAR.TABLE_NAME

    # identity fields
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # personal details
    name = db.Column(db.String)
    start_time = db.Column(db.TIMESTAMP, default=datetime.now())
    duration = db.Column(db.FLOAT)

    # relationship details
    instructor_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f"{constants.USER.TABLE_NAME}.id", ondelete="CASCADE"))
    instructor = db.relationship(
        constants.USER.OBJ_NAME, back_populates="webinars"
    )

    course_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f"{constants.COURSE.TABLE_NAME}.id", ondelete="CASCADE"))
    subject_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f"{constants.SUBJECT.TABLE_NAME}.id", ondelete="CASCADE"))
    tag_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f"{constants.TAG.TABLE_NAME}.id", ondelete="CASCADE"))

    view_count = db.Column(db.Integer)
