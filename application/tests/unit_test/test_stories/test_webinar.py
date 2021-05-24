from datetime import datetime

import pytest

from application.extensions import db
from application.models.user.constants import INSTRUCTOR
from application.models.user.constants import STUDENT
from application.models.webinar.sql import Webinar
from application.tests.factories.course import CourseFactory
from application.tests.factories.subject import SubjectFactory
from application.tests.factories.tag import TagFactory
from application.tests.factories.user import UserFactory
from application.tests.factories.webinar import WebinarFactory

# please look for webinar being filtered by courses, subjects and tags @line:171

# Instructor related test stories
def test_instructor_can_add_tag_while_uploading_webinar(app):
    instructor = UserFactory(role=INSTRUCTOR)
    tag = TagFactory(instructor=instructor)
    response = app.post(
        "/api/webinars",
        json={
            "data": {
                "type": "webinar",
                "attributes": {
                    "title": "test-webinar-2",
                    "instructor_id": instructor.id,
                    "duration": 60,
                },
                "relationships": {"tag": {"data": {"type": "tag", "id": tag.id}}},
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 201
    webinar = Webinar.query.filter_by(
        title="test-webinar-2", instructor_id=instructor.id
    ).scalar()
    assert str(webinar.id) == response.json["data"]["id"]
    # tag attached while creating webinar is assigned to the webinar
    assert webinar.tag == tag


def test_instructor_can_update_webinar(app):
    instructor = UserFactory(role=INSTRUCTOR)
    webinar = WebinarFactory(instructor=instructor)

    updated_title = "updated_title"
    response = app.patch(
        f"/api/webinars/{webinar.id}",
        json={
            "data": {
                "type": "webinar",
                "id": webinar.id,
                "attributes": {"title": updated_title},
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert webinar title gets updated
    assert webinar.title == updated_title


def test_instructor_can_delete_webinar(app):
    instructor = UserFactory(role=INSTRUCTOR)
    webinar = WebinarFactory(instructor=instructor)
    webinar_id = webinar.id

    response = app.delete(
        f"/api/webinars/{webinar.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert webinar is deleted
    assert Webinar.query.get(webinar_id) is None


# Student related test stories
def test_student_can_see_list_of_webinars(app):
    student = UserFactory(role=STUDENT)
    # upload 10 webinars
    WebinarFactory.create_batch(10)

    response = app.get(
        f"/api/webinars",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # student is able to see list of all 10 webinars
    assert response.json["meta"]["count"] == 10


def test_student_can_search_webinar_by_exact_title(app):
    student = UserFactory(role=STUDENT)
    WebinarFactory.create_batch(10)

    webinar_title = Webinar.query.all()[0].title
    query_param = f"filter[title]={webinar_title}"
    response = app.get(
        f"/api/webinars?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    assert response.json["data"][0]["id"] == str(
        Webinar.query.filter_by(title=f"{webinar_title}").scalar().id
    )


def test_student_can_search_webinar_by_similar_titles(app):
    student = UserFactory(role=STUDENT)
    WebinarFactory.create_batch(10)
    for c in range(1, 11):
        WebinarFactory(title=f"random_webinar_{c}")

    query_param = 'filter=[{"name":"title","op":"match","val":"test_webinar"}]'
    response = app.get(
        f"/api/webinars?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    # it returns only matching title webinars
    assert response.json["meta"]["count"] == 10


@pytest.mark.skip(
    reason="when run in sequence with other unit test its failing, so run it standalone"
)
def test_student_can_sort_webinars_by_view_count(app):
    student = UserFactory(role=STUDENT)

    for view_count in range(2, 11):
        WebinarFactory(view_count=view_count * 2)

    query_param = f"sort=view_count"
    response = app.get(
        f"/api/webinars?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    webinars = Webinar.query.order_by(Webinar.view_count).all()
    # videos are retrieved in increasing view_count
    for index, webinar in enumerate(response.json["data"]):
        assert webinar["id"] == str(webinars[index].id)


# filter webinars by course
def test_student_can_filter_webinar_by_course(app):
    student = UserFactory(role=STUDENT)
    # create course
    course_1 = CourseFactory()
    course_2 = CourseFactory()
    for v in range(1, 11):
        webinar = WebinarFactory()
        webinar.course_id = course_1.id

    for v in range(1, 11):
        webinar = WebinarFactory()
        webinar.course_id = course_2.id
    db.session.commit()

    response = app.get(
        f'/api/webinars?filter=[{{"name":"course_id","op":"eq","val":"{str(course_1.id)}"}}]',
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # only those webinars are included who belong to course_1
    assert response.json["meta"]["count"] == 10
    payload_webinar_ids = [webinar_data["id"] for webinar_data in response.json["data"]]
    database_webinar_ids = [
        str(webinar.id)
        for webinar in Webinar.query.filter_by(course_id=course_1.id).all()
    ]
    assert all(
        list(
            filter(
                lambda webinar_id: webinar_id in database_webinar_ids,
                payload_webinar_ids,
            )
        )
    )


def test_student_can_filter_webinar_by_subject(app):
    student = UserFactory(role=STUDENT)
    # create subject
    subject_1 = SubjectFactory()
    subject_2 = SubjectFactory()

    for _ in range(1, 11):
        webinar = WebinarFactory()
        webinar.subject_id = subject_1.id

    for _ in range(1, 11):
        webinar = WebinarFactory()
        webinar.subject_id = subject_2.id
    db.session.commit()

    response = app.get(
        f'/api/webinars?filter=[{{"name":"subject_id","op":"eq","val":"{str(subject_1.id)}"}}]',
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # only those webinars are included who belong to subject_1
    assert response.json["meta"]["count"] == 10
    payload_webinar_ids = [webinar_data["id"] for webinar_data in response.json["data"]]
    database_webinar_ids = [
        str(webinar.id)
        for webinar in Webinar.query.filter_by(course_id=subject_1.id).all()
    ]
    assert all(
        list(
            filter(
                lambda webinar_id: webinar_id in database_webinar_ids,
                payload_webinar_ids,
            )
        )
    )


def test_student_can_filter_webinar_by_tag(app):
    student = UserFactory(role=STUDENT)
    # create tag
    tag_1 = TagFactory()
    tag_2 = TagFactory()

    for _ in range(1, 11):
        webinar = WebinarFactory()
        webinar.tag_id = tag_1.id

    for _ in range(1, 11):
        webinar = WebinarFactory()
        webinar.tag_id = tag_2.id
    db.session.commit()

    response = app.get(
        f'/api/webinars?filter=[{{"name":"tag_id","op":"eq","val":"{str(tag_1.id)}"}}]',
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # only those webinars are included who belong to tag_1
    assert response.json["meta"]["count"] == 10
    payload_webinar_ids = [webinar_data["id"] for webinar_data in response.json["data"]]
    database_webinar_ids = [
        str(webinar.id) for webinar in Webinar.query.filter_by(course_id=tag_1.id).all()
    ]
    assert all(
        list(
            filter(
                lambda webinar_id: webinar_id in database_webinar_ids,
                payload_webinar_ids,
            )
        )
    )


# Negation unit test for student
def test_student_cannot_upload_webinar(app):
    student = UserFactory(role=STUDENT)
    response = app.post(
        "/api/webinars",
        json={
            "data": {
                "type": "webinar",
                "attributes": {
                    "title": "test-webinar-2",
                    "instructor_id": student.id,
                    "duration": 60,
                },
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


def test_student_cannot_update_webinar(app):
    student = UserFactory(role=STUDENT)
    webinar = WebinarFactory(instructor=student)

    updated_title = "updated_title"
    response = app.patch(
        f"/api/webinars/{webinar.id}",
        json={
            "data": {
                "type": "webinar",
                "id": webinar.id,
                "attributes": {"title": updated_title},
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
        == "Only Instructors are allowed to update webinar"
    )


def test_student_cannot_delete_webinar(app):
    student = UserFactory(role=STUDENT)
    webinar = WebinarFactory(instructor=student)
    response = app.delete(
        f"/api/webinars/{webinar.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 403
    assert response.json["errors"][0]["title"] == "Access denied"
    assert (
        response.json["errors"][0]["source"]
        == "Only Instructors are allowed to delete webinar"
    )
