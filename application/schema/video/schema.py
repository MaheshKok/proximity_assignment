from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class VideoSchema(Schema):
    class Meta:
        type_ = "video"
        self_view = "video_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "video_list"

    id = fields.UUID(as_string=True, dump_only=True)
    name = fields.Str(required=True)
    view_count = fields.Integer()

    course_id = fields.UUID(as_string=True)
    course = Relationship(
        schema="courseSchema",
        type_="course",
    )
    subject_id = fields.UUID(as_string=True)
    subject = Relationship(
        schema="subjectSchema",
        type_="subject",
    )
    tag_id = fields.UUID(as_string=True)
    tag = Relationship(
        schema="TagSchema",
        type_="tag",
    )
    instructor_id = fields.UUID(as_string=True,required=True)
    instructor = Relationship(
        schema="UserSchema",
        type_="user",
    )

