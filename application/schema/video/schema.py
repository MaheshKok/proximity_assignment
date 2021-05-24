from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from marshmallow_jsonapi.flask import Schema


class VideoSchema(Schema):
    class Meta:
        type_ = "video"
        self_view = "video_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "video_list"

    id = fields.UUID(as_string=True, dump_only=True)
    title = fields.Str(required=True, allow_none=False)
    view_count = fields.Integer(default=1, missing=1)

    course_id = fields.UUID(as_string=True, required=False)
    course = Relationship(schema="courseSchema", type_="course",)
    subject_id = fields.UUID(as_string=True, required=False)
    subject = Relationship(schema="subjectSchema", type_="subject",)
    tag_id = fields.UUID(as_string=True, required=False)
    tag = Relationship(schema="TagSchema", type_="tag",)
    instructor_id = fields.UUID(as_string=True, required=True)
    instructor = Relationship(schema="UserSchema", type_="user",)
