import logging

from flask import request
from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi import ResourceRelationship
from flask_rest_jsonapi.exceptions import AccessDenied

from application.extensions import db
from application.models.user.constants import INSTRUCTOR
from application.models.user.sql import User
from application.models.video.sql import Video
from application.schema.video.schema import VideoSchema

log = logging.getLogger(__file__)

# Create resource managers
class VideoDetail(ResourceDetail):
    schema = VideoSchema
    data_layer = {"session": db.session, "model": Video}

    def before_delete(self, args, kwargs):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to delete video: [{kwargs['id']}] by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to delete video",
            )

    def before_patch(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to update video: [{kwargs['id']}] by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to update video",
            )


class VideoList(ResourceList):
    schema = VideoSchema
    data_layer = {"session": db.session, "model": Video}

    def before_post(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to upload video by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to upload video",
            )


class VideoRelationship(ResourceRelationship):
    schema = VideoSchema
    data_layer = {"session": db.session, "model": Video}
