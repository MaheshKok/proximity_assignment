from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from application.extensions import db
from application.models import constants


class Video(db.Model):
    __tablename__ = constants.VIDEO.TABLE_NAME
    #  # this will ensure no duplicate data in database
    __table_args__ = (
        db.UniqueConstraint(
            "name",
            "instructor_id",
            "subject_id",
            "course_id",
            name="uix_video_instructor_id_subject_id_course_id",
        ),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String)

    instructor_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.USER.TABLE_NAME}.id", ondelete="CASCADE"),
    )
    instructor = db.relationship(constants.USER.OBJ_NAME, back_populates="videos")
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
