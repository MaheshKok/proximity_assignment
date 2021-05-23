from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class CourseSchema(Schema):
    class Meta:
        type_ = "course"
        self_view = "course_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "course_list"

    id = fields.UUID(as_string=True, dump_only=True)
    name = fields.Str(required=True)

    view_count = fields.Integer()
    instructor_id = fields.UUID(as_string=True, required=True)
    instructor = Relationship(schema="UserSchema", type_="user",)

    tag_id = fields.UUID(as_string=True)
    tag = Relationship(schema="TagSchema", type_="tag",)
    webinars = Relationship(schema="WebinarSchema", type_="webinar", many=True)
    videos = Relationship(schema="VideoSchema", type_="video", many=True)
