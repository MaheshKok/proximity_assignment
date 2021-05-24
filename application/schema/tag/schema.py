from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from marshmallow_jsonapi.flask import Schema


class TagSchema(Schema):
    class Meta:
        type_ = "tag"
        self_view = "tag_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "tag_list"

    id = fields.UUID(as_string=True, dump_only=True)
    title = fields.Str(required=True)

    courses = Relationship(schema="CourseSchema", type_="course", many=True)
    subjects = Relationship(schema="SubjectSchema", type_="subject", many=True)
    instructor_id = fields.UUID(as_string=True, required=True, allow_none=False)
    instructor = Relationship(schema="UserSchema", type_="user",)
    webinars = Relationship(schema="WebinarSchema", type_="webinar", many=True)
    videos = Relationship(schema="VideoSchema", type_="video", many=True)
