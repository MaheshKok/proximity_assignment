from uuid import uuid4

from sqlalchemy import event
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from application.models import constants


class Video(db.Model):
    __tablename__ = constants.VIDEO.TABLE_NAME
    #  # this will ensure no duplicate data in database
    __table_args__ = (
        db.UniqueConstraint(
            "title",
            "instructor_id",
            "subject_id",
            "course_id",
            name="uix_video_instructor_id_subject_id_course_id",
        ),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String, nullable=False)

    instructor_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.USER.TABLE_NAME}.id", ondelete="CASCADE"),
        nullable=False,
    )
    instructor = db.relationship(constants.USER.OBJ_NAME, back_populates="videos")
    course_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.COURSE.TABLE_NAME}.id", ondelete="CASCADE"),
        nullable=True,
    )
    subject_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.SUBJECT.TABLE_NAME}.id", ondelete="CASCADE"),
        nullable=True,
    )
    tag_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{constants.TAG.TABLE_NAME}.id", ondelete="CASCADE"),
        nullable=True,
    )

    view_count = db.Column(db.Integer, default=1)


@event.listens_for(Video, "after_update")
def increase_course_view_count(mapper, connection, target: Video) -> None:
    Video.view_count = target.view_count + 1
