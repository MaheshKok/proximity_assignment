from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from marshmallow_jsonapi.flask import Schema


class WebinarSchema(Schema):
    class Meta:
        type_ = "webinar"
        self_view = "webinar_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "webinar_list"

    id = fields.UUID(as_string=True, dump_only=True)
    title = fields.Str(required=True, allow_none=False)
    start_time = fields.DateTime()
    duration = fields.Integer(required=True, allow_none=False)

    view_count = fields.Integer(default=1, allow_none=False)

    course_id = fields.UUID(as_string=True, required=False, allow_none=True)
    course = Relationship(schema="courseSchema", type_="course",)
    subject_id = fields.UUID(as_string=True, required=False, allow_none=True)
    subject = Relationship(schema="subjectSchema", type_="subject",)
    tag_id = fields.UUID(as_string=True, required=False, allow_none=True)
    tag = Relationship(schema="TagSchema", type_="tag",)
    instructor_id = fields.UUID(as_string=True, required=True, allow_none=False)
    instructor = Relationship(schema="UserSchema", type_="user",)
