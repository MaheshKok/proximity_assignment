from flask_rest_jsonapi import Api

from application.blueprints.apis.course.api import CourseDetail
from application.blueprints.apis.course.api import CourseList
from application.blueprints.apis.subject.api import SubjectDetail
from application.blueprints.apis.subject.api import SubjectList
from application.blueprints.apis.tag.api import TagDetail
from application.blueprints.apis.tag.api import TagList
from application.blueprints.apis.user.api import UserDetail
from application.blueprints.apis.user.api import UserList
from application.blueprints.apis.video.api import VideoDetail
from application.blueprints.apis.video.api import VideoList
from application.blueprints.apis.webinar.api import WebinarDetail
from application.blueprints.apis.webinar.api import WebinarList


def register_json_routes(app):
    # Create endpoints
    api = Api(app)

    api.route(CourseList, "course_list", "/api/courses")
    api.route(CourseDetail, "course_detail", "/api/courses/<string:id>")

    api.route(SubjectList, "subject_list", "/api/subjects")
    api.route(SubjectDetail, "subject_detail", "/api/subjects/<string:id>")

    api.route(TagList, "tag_list", "/api/tags")
    api.route(TagDetail, "tag_detail", "/api/tags/<string:id>")

    api.route(UserList, "user_list", "/api/users")
    api.route(UserDetail, "user_detail", "/api/users/<string:id>")

    api.route(VideoList, "video_list", "/api/videos")
    api.route(VideoDetail, "video_detail", "/api/videos/<string:id>")

    api.route(WebinarList, "webinar_list", "/api/webinars")
    api.route(WebinarDetail, "webinar_detail", "/api/webinars/<string:id>")
