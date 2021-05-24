from application.models.tag.sql import Tag
from application.models.user.constants import INSTRUCTOR
from application.models.user.constants import STUDENT
from application.tests.factories.tag import TagFactory
from application.tests.factories.user import UserFactory


# Instructor related test stories
def test_instructor_can_create_tag(app):
    instructor = UserFactory(role=INSTRUCTOR)
    response = app.post(
        "/api/tags",
        json={
            "data": {
                "type": "tag",
                "attributes": {"title": "test-tag-2", "instructor_id": instructor.id},
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
            Tag.query.filter_by(title="test-tag-2", instructor_id=instructor.id)
            .scalar()
            .id
        )
        == response.json["data"]["id"]
    )


def test_instructor_can_update_tag(app):
    instructor = UserFactory(role=INSTRUCTOR)
    tag = TagFactory(instructor=instructor)

    updated_title = "updated_title"
    response = app.patch(
        f"/api/tags/{tag.id}",
        json={
            "data": {
                "type": "tag",
                "id": tag.id,
                "attributes": {"title": updated_title},
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert tag name gets updated
    assert tag.title == updated_title


def test_instructor_can_delete_tag(app):
    instructor = UserFactory(role=INSTRUCTOR)
    tag = TagFactory(instructor=instructor)
    tag_id = tag.id

    response = app.delete(
        f"/api/tags/{tag.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert tag is deleted
    assert Tag.query.get(tag_id) is None


# Student related test stories
def test_student_can_see_list_of_tags(app):
    student = UserFactory(role=STUDENT)
    # create 10 tags
    TagFactory.create_batch(10)

    response = app.get(
        f"/api/tags",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # student is able to see list of all 10 tags
    assert response.json["meta"]["count"] == 10


def test_student_can_search_tag_by_exact_title(app):
    student = UserFactory(role=STUDENT)
    TagFactory.create_batch(10)

    query_param = "filter[title]=test_tag_1"
    response = app.get(
        f"/api/tags?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    assert response.json["data"][0]["id"] == str(
        Tag.query.filter_by(title="test_tag_1").scalar().id
    )


def test_student_can_search_tag_by_similar_titles(app):
    student = UserFactory(role=STUDENT)
    TagFactory.create_batch(10)
    for c in range(1, 11):
        TagFactory(title=f"random_tag_{c}")

    query_param = 'filter=[{"name":"title","op":"match","val":"test_tag"}]'
    response = app.get(
        f"/api/tags?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    # it returns only matching title tags
    assert response.json["meta"]["count"] == 10
