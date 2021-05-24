import logging

from flask import request
from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi import ResourceRelationship
from flask_rest_jsonapi.exceptions import AccessDenied

from application.extensions import db
from application.models.course.sql import Course
from application.models.user.constants import INSTRUCTOR
from application.models.user.sql import User
from application.schema.course.schema import CourseSchema

log = logging.getLogger(__file__)

# Create resource managers
class CourseDetail(ResourceDetail):
    schema = CourseSchema
    data_layer = {"session": db.session, "model": Course}

    def before_delete(self, args, kwargs):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to delete course: [{kwargs['id']}] by student: [{logged_in_user.id}]"
            )
            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to delete course",
            )

    def before_patch(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to update course: [{kwargs['id']}] by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to update course",
            )


class CourseList(ResourceList):
    schema = CourseSchema
    data_layer = {"session": db.session, "model": Course}

    def before_post(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            log.exception(
                f"Access Denied when attempting to create course by student: [{logged_in_user.id}]"
            )

            raise AccessDenied(
                {"parameter": "logged_in_user_id"},
                "Only Instructors are allowed to create course",
            )


class CourseRelationship(ResourceRelationship):
    schema = CourseSchema
    data_layer = {"session": db.session, "model": Course}
