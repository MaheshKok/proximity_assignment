"""
this file contains many to many relationship between models
"""
from sqlalchemy.dialects.postgresql import UUID
from application.extensions import db
from application.models import constants

#
# webinar_courses = db.Table(
#     "webinar_courses",
#     db.metadata,
#     db.Column(
#         f"{constants.WEBINAR.TABLE_NAME}_id",
#         UUID(as_uuid=True),
#         db.ForeignKey(f"{constants.WEBINAR.TABLE_NAME}.id", ondelete="CASCADE"),
#     ),
#     db.Column(
#         f"{constants.COURSE.TABLE_NAME}_id",
#         UUID(as_uuid=True),
#         db.ForeignKey(f"{constants.COURSE.TABLE_NAME}.id", ondelete="CASCADE"),
#     ),
# )
#
#
# webinar_subjects = db.Table(
#     "webinar_subjects",
#     db.metadata,
#     db.Column(
#         f"{constants.WEBINAR.TABLE_NAME}_id",
#         UUID(as_uuid=True),
#         db.ForeignKey(f"{constants.WEBINAR.TABLE_NAME}.id", ondelete="CASCADE"),
#     ),
#     db.Column(
#         f"{constants.SUBJECT.TABLE_NAME}_id",
#         UUID(as_uuid=True),
#         db.ForeignKey(f"{constants.SUBJECT.TABLE_NAME}.id", ondelete="CASCADE"),
#     ),
# )
#
