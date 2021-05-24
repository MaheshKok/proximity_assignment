from application.models.subject.sql import Subject
from application.models.user.constants import INSTRUCTOR
from application.models.user.constants import STUDENT
from application.tests.factories.subject import SubjectFactory
from application.tests.factories.user import UserFactory


# Instructor related test stories
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


# Student related test stories
def test_student_can_see_list_of_subjects(app):
    student = UserFactory(role=STUDENT)
    # create 10 subjects
    SubjectFactory.create_batch(10)

    response = app.get(
        f"/api/subjects",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # student is able to see list of all 10 subjects
    assert response.json["meta"]["count"] == 10


def test_student_can_search_subject_by_exact_title(app):
    student = UserFactory(role=STUDENT)
    SubjectFactory.create_batch(10)

    subject_title = Subject.query.all()[0].title
    query_param = f"filter[title]={subject_title}"
    response = app.get(
        f"/api/subjects?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    assert response.json["data"][0]["id"] == str(
        Subject.query.filter_by(title=f"{subject_title}").scalar().id
    )


def test_student_can_search_subject_by_similar_titles(app):
    student = UserFactory(role=STUDENT)
    SubjectFactory.create_batch(10)
    for c in range(1, 11):
        SubjectFactory(title=f"random_subject_{c}")

    query_param = 'filter=[{"name":"title","op":"match","val":"test_subject"}]'
    response = app.get(
        f"/api/subjects?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    # it returns only matching title subjects
    assert response.json["meta"]["count"] == 10


# Negation unit test for student
def test_student_cannot_create_subject(app):
    student = UserFactory(role=STUDENT)
    response = app.post(
        "/api/subjects",
        json={
            "data": {
                "type": "subject",
                "attributes": {"title": "test-course-2", "instructor_id": student.id},
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
        == "Only Instructors are allowed to create subject"
    )


def test_student_cannot_update_subject(app):
    student = UserFactory(role=STUDENT)
    subject = SubjectFactory(instructor=student)

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
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 403
    assert response.json["errors"][0]["title"] == "Access denied"
    assert (
        response.json["errors"][0]["source"]
        == "Only Instructors are allowed to update subject"
    )


def test_student_cannot_delete_subject(app):
    student = UserFactory(role=STUDENT)
    subject = SubjectFactory(instructor=student)
    response = app.delete(
        f"/api/subjects/{subject.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 403
    assert response.json["errors"][0]["title"] == "Access denied"
    assert (
        response.json["errors"][0]["source"]
        == "Only Instructors are allowed to delete subject"
    )
