from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from marshmallow_jsonapi.flask import Schema


class CourseSchema(Schema):
    class Meta:
        type_ = "course"
        self_view = "course_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "course_list"

    id = fields.UUID(as_string=True, dump_only=True)
    title = fields.Str(required=True, allow_none=False)

    # the one who would be uploading course will be the first viewer hence view_count defaults to 1
    view_count = fields.Integer(default=1)
    instructor_id = fields.UUID(as_string=True, required=True, allow_none=False)
    instructor = Relationship(schema="UserSchema", type_="user",)

    tag_id = fields.UUID(as_string=True, required=False)
    tag = Relationship(schema="TagSchema", type_="tag",)
    webinars = Relationship(schema="WebinarSchema", type_="webinar", many=True)
    videos = Relationship(schema="VideoSchema", type_="video", many=True)
