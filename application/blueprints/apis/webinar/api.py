import logging

from flask import request
from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi import ResourceRelationship
from flask_rest_jsonapi.exceptions import AccessDenied

from application.extensions import db
from application.models.user.constants import INSTRUCTOR
from application.models.user.sql import User
from application.models.webinar.sql import Webinar
from application.schema.webinar.schema import WebinarSchema

log = logging.getLogger(__file__)
# Create resource managers
class WebinarDetail(ResourceDetail):
    schema = WebinarSchema
    data_layer = {"session": db.session, "model": Webinar}

    def before_delete(self, args, kwargs):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to delete webinar: [{kwargs['id']}] by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to delete webinar",
            )

    def before_patch(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to update webinar: [{kwargs['id']}] by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to update webinar",
            )


class WebinarList(ResourceList):
    schema = WebinarSchema
    data_layer = {"session": db.session, "model": Webinar}

    def before_post(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to upload webinar by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to upload webinar",
            )


class WebinarRelationship(ResourceRelationship):
    schema = WebinarSchema
    data_layer = {"session": db.session, "model": Webinar}
