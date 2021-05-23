from flask import request
from flask_rest_jsonapi import ResourceDetail, ResourceRelationship, ResourceList
from flask_rest_jsonapi.exceptions import AccessDenied

from application.extensions import db
from application.models.tag.sql import Tag
from application.models.user.constants import INSTRUCTOR
from application.models.user.sql import User
from application.schema.tag.schema import TagSchema


class TagDetail(ResourceDetail):
    schema = TagSchema
    data_layer = {"session": db.session, "model": Tag}

    def before_delete(self, args, kwargs):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                f"Only Instructors are allowed to delete tag",
            )

    def before_patch(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                f"Only Instructors are allowed to update tag",
            )


class TagList(ResourceList):
    schema = TagSchema
    data_layer = {"session": db.session, "model": Tag}


class TagRelationship(ResourceRelationship):
    schema = TagSchema
    data_layer = {"session": db.session, "model": Tag}
