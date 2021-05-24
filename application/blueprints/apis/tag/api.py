import logging

from flask import request
from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi import ResourceRelationship
from flask_rest_jsonapi.exceptions import AccessDenied

from application.extensions import db
from application.models.tag.sql import Tag
from application.models.user.constants import INSTRUCTOR
from application.models.user.sql import User
from application.schema.tag.schema import TagSchema

log = logging.getLogger(__file__)

# Create resource managers
class TagDetail(ResourceDetail):
    schema = TagSchema
    data_layer = {"session": db.session, "model": Tag}

    def before_delete(self, args, kwargs):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to delete tag: [{kwargs['id']}] by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to delete tag",
            )

    def before_patch(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to update tag: [{kwargs['id']}] by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to update tag",
            )


class TagList(ResourceList):
    schema = TagSchema
    data_layer = {"session": db.session, "model": Tag}

    def before_post(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to create tag by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to create tag",
            )


class TagRelationship(ResourceRelationship):
    schema = TagSchema
    data_layer = {"session": db.session, "model": Tag}
