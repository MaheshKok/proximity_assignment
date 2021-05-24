from flask import request
from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi import ResourceRelationship
from flask_rest_jsonapi.exceptions import AccessDenied

from application.extensions import db
from application.models.subject.sql import Subject
from application.models.user.constants import INSTRUCTOR
from application.models.user.sql import User
from application.schema.subject.schema import SubjectSchema


# Create resource managers
class SubjectDetail(ResourceDetail):
    schema = SubjectSchema
    data_layer = {"session": db.session, "model": Subject}

    def before_delete(self, args, kwargs):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to delete subject",
            )

    def before_patch(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to update subject",
            )


class SubjectList(ResourceList):
    schema = SubjectSchema
    data_layer = {"session": db.session, "model": Subject}

    def before_post(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to create subject",
            )


class SubjectRelationship(ResourceRelationship):
    schema = SubjectSchema
    data_layer = {"session": db.session, "model": Subject}
