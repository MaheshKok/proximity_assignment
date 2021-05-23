from flask import request
from flask_rest_jsonapi import ResourceDetail, ResourceRelationship, ResourceList
from flask_rest_jsonapi.exceptions import AccessDenied

from application.extensions import db
from application.models.user.constants import INSTRUCTOR
from application.models.user.sql import User
from application.models.video.sql import Video
from application.schema.video.schema import VideoSchema


class VideoDetail(ResourceDetail):
    schema = VideoSchema
    data_layer = {"session": db.session, "model": Video}

    def before_delete(self, args, kwargs):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"}, f"Only Instructors are allowed to delete video"
            )

    def before_patch(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"}, f"Only Instructors are allowed to edit video"
            )


class VideoList(ResourceList):
    schema = VideoSchema
    data_layer = {"session": db.session, "model": Video}




class VideoRelationship(ResourceRelationship):
    schema = VideoSchema
    data_layer = {"session": db.session, "model": Video}