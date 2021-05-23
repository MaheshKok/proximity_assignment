from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class SubjectSchema(Schema):
    class Meta:
        type_ = "subject"
        self_view = "subject_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "subject_list"

    id = fields.UUID(as_string=True, dump_only=True)
    name = fields.Str(required=True)

    instructor_id = fields.UUID(as_string=True, required=True)
    instructor = Relationship(schema="UserSchema", type_="user",)

    tag_id = fields.UUID(as_string=True)
    tag = Relationship(schema="TagSchema", type_="tag",)
    webinars = Relationship(schema="WebinarSchema", type_="webinar", many=True)
    videos = Relationship(schema="VideoSchema", type_="video", many=True)
