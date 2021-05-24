
# Instructor related test stories
from application.models.subject.sql import Subject
from application.models.user.constants import INSTRUCTOR
from application.tests.factories.subject import SubjectFactory
from application.tests.factories.user import UserFactory


def test_instructor_can_create_subject(app):
    instructor = UserFactory(role=INSTRUCTOR)
    response = app.post(
        "/api/subjects",
        json={
            "data": {
                "type": "subject",
                "attributes": {
                    "title": "test-subject-2",
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
            Subject.query.filter_by(title="test-subject-2", instructor_id=instructor.id)
            .scalar()
            .id
        )
        == response.json["data"]["id"]
    )


def test_instructor_can_update_subject(app):
    instructor = UserFactory(role=INSTRUCTOR)
    subject = SubjectFactory(instructor=instructor)

    updated_title = "updated_title"
    response = app.patch(
        f"/api/subjects/{subject.id}",
        json={
            "data": {
                "type": "subject",
                "id": subject.id,
                "attributes": {"title": updated_title},
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert subject name gets updated
    assert subject.title == updated_title


def test_instructor_can_delete_subject(app):
    instructor = UserFactory(role=INSTRUCTOR)
    subject = SubjectFactory(instructor=instructor)
    subject_id = subject.id

    response = app.delete(
        f"/api/subjects/{subject.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert subject is deleted
    assert Subject.query.get(subject_id) is None
