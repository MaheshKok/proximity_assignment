from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from marshmallow_jsonapi.flask import Schema


class UserSchema(Schema):
    class Meta:
        type_ = "user"
        self_view = "user_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "user_list"

    id = fields.UUID(as_string=True, dump_only=True)
    title = fields.Str(required=True, allow_none=False)
    role = fields.Str(required=True, allow_none=False)

    courses = Relationship(schema="CourseSchema", type_="course", many=True)
    subjects = Relationship(schema="SubjectSchema", type_="subject", many=True)
    tags = Relationship(schema="TagSchema", type_="tag", many=True)
    videos = Relationship(schema="VideoSchema", type_="video", many=True)
    webinars = Relationship(schema="WebinarSchema", type_="webinar", many=True)
