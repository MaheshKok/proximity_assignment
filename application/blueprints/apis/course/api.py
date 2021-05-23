from flask import request
from flask_rest_jsonapi import ResourceDetail, ResourceRelationship, ResourceList
from flask_rest_jsonapi.exceptions import AccessDenied

from application.extensions import db
from application.models.course.sql import Course
from application.models.user.constants import INSTRUCTOR
from application.models.user.sql import User
from application.schema.course.schema import CourseSchema


class CourseDetail(ResourceDetail):
    schema = CourseSchema
    data_layer = {"session": db.session, "model": Course}

    def before_delete(self, args, kwargs):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"}, f"Only Instructors are allowed to delete course"
            )

    def before_patch(self, args, kwargs, data=None):
        logged_in_user = User.query.get(request.headers.get("logged_in_user_id"))
        if logged_in_user.role != INSTRUCTOR:
            raise AccessDenied(
                {"parameter": "logged_in_user_id"}, f"Only Instructors are allowed to update course"
            )


class CourseList(ResourceList):
    schema = CourseSchema
    data_layer = {"session": db.session, "model": Course}


class CourseRelationship(ResourceRelationship):
    schema = CourseSchema
    data_layer = {"session": db.session, "model": Course}

