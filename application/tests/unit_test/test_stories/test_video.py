import pytest

from application.extensions import db
from application.models.user.constants import INSTRUCTOR
from application.models.user.constants import STUDENT
from application.models.video.sql import Video
from application.tests.factories.course import CourseFactory
from application.tests.factories.subject import SubjectFactory
from application.tests.factories.tag import TagFactory
from application.tests.factories.user import UserFactory
from application.tests.factories.video import VideoFactory


# please look for video being filtered by courses, subjects and tags @line:165
# Instructor related test stories
def test_instructor_can_add_tag_while_uploading_video(app):
    instructor = UserFactory(role=INSTRUCTOR)
    tag = TagFactory(instructor=instructor)
    response = app.post(
        "/api/videos",
        json={
            "data": {
                "type": "video",
                "attributes": {"title": "test-video-2", "instructor_id": instructor.id},
                "relationships": {"tag": {"data": {"type": "tag", "id": tag.id}}},
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 201
    video = Video.query.filter_by(
        title="test-video-2", instructor_id=instructor.id
    ).scalar()
    assert str(video.id) == response.json["data"]["id"]
    # tag attached while creating video is assigned to the video
    assert video.tag == tag


def test_instructor_can_update_video(app):
    instructor = UserFactory(role=INSTRUCTOR)
    video = VideoFactory(instructor=instructor)

    updated_title = "updated_title"
    response = app.patch(
        f"/api/videos/{video.id}",
        json={
            "data": {
                "type": "video",
                "id": video.id,
                "attributes": {"title": updated_title},
            }
        },
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert video name gets updated
    assert video.title == updated_title


def test_instructor_can_delete_video(app):
    instructor = UserFactory(role=INSTRUCTOR)
    video = VideoFactory(instructor=instructor)
    video_id = video.id

    response = app.delete(
        f"/api/videos/{video.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": instructor.id,
        },
    )
    assert response.status_code == 200
    # assert video is deleted
    assert video.query.get(video_id) is None


# Student related test stories
def test_student_can_see_list_of_videos(app):
    student = UserFactory(role=STUDENT)
    # upload 10 videos
    VideoFactory.create_batch(10)

    response = app.get(
        f"/api/videos",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # student is able to see list of all 10 videos
    assert response.json["meta"]["count"] == 10


def test_student_can_search_video_by_exact_title(app):
    student = UserFactory(role=STUDENT)
    VideoFactory.create_batch(10)

    video_title = Video.query.all()[0].title
    query_param = f"filter[title]={video_title}"
    response = app.get(
        f"/api/videos?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    assert response.json["data"][0]["id"] == str(
        Video.query.filter_by(title=f"{video_title}").scalar().id
    )


def test_student_can_search_video_by_similar_titles(app):
    student = UserFactory(role=STUDENT)
    VideoFactory.create_batch(10)
    for c in range(1, 11):
        VideoFactory(title=f"random_video_{c}")

    query_param = 'filter=[{"name":"title","op":"match","val":"test_video"}]'
    response = app.get(
        f"/api/videos?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    # it returns only matching title videos
    assert response.json["meta"]["count"] == 10


@pytest.mark.skip(
    reason="when run in sequence with other unit test its failing, so run it standalone"
)
def test_student_can_sort_videos_by_view_count(app):
    student = UserFactory(role=STUDENT)

    for view_count in range(2, 11):
        VideoFactory(view_count=view_count * 2)

    query_param = f"sort=view_count"
    response = app.get(
        f"/api/videos?{query_param}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 200
    videos = Video.query.order_by(Video.view_count).all()
    # videos are retrieved in increasing view_count
    for index, video in enumerate(response.json["data"]):
        assert video["id"] == str(videos[index].id)


# filter videos by course
def test_student_can_filter_video_by_course(app):
    student = UserFactory(role=STUDENT)
    # create course
    course_1 = CourseFactory()
    course_2 = CourseFactory()
    for v in range(1, 11):
        video = VideoFactory()
        video.course_id = course_1.id

    for v in range(1, 11):
        video = VideoFactory()
        video.course_id = course_2.id
    db.session.commit()

    response = app.get(
        f'/api/videos?filter=[{{"name":"course_id","op":"eq","val":"{str(course_1.id)}"}}]',
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # only those videos are included who belong to course_1
    assert response.json["meta"]["count"] == 10
    payload_video_ids = [video_data["id"] for video_data in response.json["data"]]
    database_video_ids = [
        str(video.id) for video in Video.query.filter_by(course_id=course_1.id).all()
    ]
    assert all(
        list(filter(lambda video_id: video_id in database_video_ids, payload_video_ids))
    )


def test_student_can_filter_video_by_subject(app):
    student = UserFactory(role=STUDENT)
    # create subject
    subject_1 = SubjectFactory()
    subject_2 = SubjectFactory()

    for _ in range(1, 11):
        video = VideoFactory()
        video.subject_id = subject_1.id

    for _ in range(1, 11):
        video = VideoFactory()
        video.subject_id = subject_2.id
    db.session.commit()

    response = app.get(
        f'/api/videos?filter=[{{"name":"subject_id","op":"eq","val":"{str(subject_1.id)}"}}]',
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # only those videos are included who belong to subject_1
    assert response.json["meta"]["count"] == 10
    payload_video_ids = [video_data["id"] for video_data in response.json["data"]]
    database_video_ids = [
        str(video.id) for video in Video.query.filter_by(course_id=subject_1.id).all()
    ]
    assert all(
        list(filter(lambda video_id: video_id in database_video_ids, payload_video_ids))
    )


def test_student_can_filter_video_by_tag(app):
    student = UserFactory(role=STUDENT)
    # create tag
    tag_1 = TagFactory()
    tag_2 = TagFactory()

    for _ in range(1, 11):
        video = VideoFactory()
        video.tag_id = tag_1.id

    for _ in range(1, 11):
        video = VideoFactory()
        video.tag_id = tag_2.id
    db.session.commit()

    response = app.get(
        f'/api/videos?filter=[{{"name":"tag_id","op":"eq","val":"{str(tag_1.id)}"}}]',
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )

    assert response.status_code == 200
    # only those videos are included who belong to tag_1
    assert response.json["meta"]["count"] == 10
    payload_video_ids = [video_data["id"] for video_data in response.json["data"]]
    database_video_ids = [
        str(video.id) for video in Video.query.filter_by(course_id=tag_1.id).all()
    ]
    assert all(
        list(filter(lambda video_id: video_id in database_video_ids, payload_video_ids))
    )


# Negation unit test for student
def test_student_cannot_upload_video(app):
    student = UserFactory(role=STUDENT)
    response = app.post(
        "/api/videos",
        json={
            "data": {
                "type": "video",
                "attributes": {"title": "test-video-2", "instructor_id": student.id},
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
        == "Only Instructors are allowed to upload video"
    )


def test_student_cannot_update_video(app):
    student = UserFactory(role=STUDENT)
    video = VideoFactory(instructor=student)

    updated_title = "updated_title"
    response = app.patch(
        f"/api/videos/{video.id}",
        json={
            "data": {
                "type": "video",
                "id": video.id,
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
        == "Only Instructors are allowed to update video"
    )


def test_student_cannot_delete_video(app):
    student = UserFactory(role=STUDENT)
    video = VideoFactory(instructor=student)
    response = app.delete(
        f"/api/videos/{video.id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "logged_in_user_id": student.id,
        },
    )
    assert response.status_code == 403
    assert response.json["errors"][0]["title"] == "Access denied"
    assert (
        response.json["errors"][0]["source"]
        == "Only Instructors are allowed to delete video"
    )
