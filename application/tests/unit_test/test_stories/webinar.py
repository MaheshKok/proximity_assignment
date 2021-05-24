from application.models.user.constants import INSTRUCTOR
from application.models.user.constants import STUDENT
from application.models.webinar.sql import Webinar
from application.tests.factories.user import UserFactory


def test_instructor_can_upload_webinar(app):
    instructor = UserFactory(role=INSTRUCTOR)
    response = app.post(
        "/api/webinars",
        json={
            "data": {
                "type": "webinar",
                "attributes": {
                    "title": "test-webinar-2",
                    "instructor_id": instructor.id,
                },
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 201
    assert (
        str(
            Webinar.query.filter_by(name="test-webinar-2", instructor_id=instructor.id)
            .scalar()
            .id
        )
        == response.json["data"]["id"]
    )


def test_student_cannot_upload_webinar(app):
    student = UserFactory(role=STUDENT)
    response = app.post(
        "/api/webinars",
        json={
            "data": {
                "type": "webinar",
                "attributes": {"title": "test-webinar-2", "instructor_id": student.id},
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 403
    assert response.json["errors"][0]["title"] == "Access denied"
    assert (
        response.json["errors"][0]["source"]
        == "Only Instructors are allowed to upload webinar"
    )
