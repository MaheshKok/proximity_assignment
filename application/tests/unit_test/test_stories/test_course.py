from application.models.course.sql import Course
from application.models.user.constants import INSTRUCTOR
from application.models.user.constants import STUDENT
from application.tests.factories.course import CourseFactory
from application.tests.factories.user import UserFactory


# Instructor related test stories
def test_instructor_can_create_course(app):
    instructor = UserFactory(role=INSTRUCTOR)
    response = app.post(
        "/api/courses",
        json={
            "data": {
                "type": "course",
                "attributes": {
                    "title": "test-course-2",
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
            Course.query.filter_by(title="test-course-2", instructor_id=instructor.id)
            .scalar()
            .id
        )
        == response.json["data"]["id"]
    )


def test_instructor_can_update_course(app):
    instructor = UserFactory(role=INSTRUCTOR)
    course = CourseFactory(instructor=instructor)

    updated_title = "updated_title"
    response = app.patch(
        f"/api/courses/{course.id}",
        json={
            "data": {
                "type": "course",
                "id": course.id,
                "attributes": {"title": updated_title},
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert course name gets updated
    assert course.name == updated_title


def test_instructor_can_delete_course(app):
    instructor = UserFactory(role=INSTRUCTOR)
    course = CourseFactory(instructor=instructor)
    course_id = course.id

    response = app.delete(
        f"/api/courses/{course.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert course is deleted
    assert Course.query.get(course_id) is None


# Student related test stories
def test_student_can_see_list_of_courses(app):
    student = UserFactory(role=STUDENT)
    # create 10 courses
    CourseFactory.create_batch(10)

    response = app.get(
        f"/api/courses",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # student is able to see list of all 10 courses
    assert response.json["meta"]["count"] == 10


def test_student_can_search_course_by_exact_title(app):
    student = UserFactory(role=STUDENT)
    CourseFactory.create_batch(10)

    query_param = "filter[title]=test_course_1"
    response = app.get(
        f"/api/courses?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    assert response.json["data"][0]["id"] == str(
        Course.query.filter_by(title="test_course_1").scalar().id
    )


def test_student_can_search_course_by_similar_titles(app):
    student = UserFactory(role=STUDENT)
    CourseFactory.create_batch(10)
    for c in range(1, 11):
        CourseFactory(title=f"random_course_{c}")

    query_param = 'filter=[{"name":"title","op":"match","val":"test_course"}]'
    response = app.get(
        f"/api/courses?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    # it returns only matching title courses
    assert response.json["meta"]["count"] == 10


# Negation unit test for student
def test_student_cannot_upload_course(app):
    student = UserFactory(role=STUDENT)
    response = app.post(
        "/api/courses",
        json={
            "data": {
                "type": "course",
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
        == "Only Instructors are allowed to create course"
    )


def test_student_cannot_update_course(app):
    student = UserFactory(role=STUDENT)
    course = CourseFactory(instructor=student)

    updated_title = "updated_title"
    response = app.patch(
        f"/api/courses/{course.id}",
        json={
            "data": {
                "type": "course",
                "id": course.id,
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
        == "Only Instructors are allowed to update course"
    )


def test_student_cannot_delete_course(app):
    student = UserFactory(role=STUDENT)
    course = CourseFactory(instructor=student)
    response = app.delete(
        f"/api/courses/{course.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 403
    assert response.json["errors"][0]["title"] == "Access denied"
    assert (
        response.json["errors"][0]["source"]
        == "Only Instructors are allowed to delete course"
    )
