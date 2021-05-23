from application.tests.factories.user import UserFactory


def test_webinar(app):
    instructor = UserFactory()
    response = app.post(
        "/api/webinars",
        json={
            "data": {
                "type": "webinar",
                "attributes": {
                    "name": "test-webinar-2",
                    "instructor_id": instructor.id,
                },
            }
        },
        headers={"Content-Type": "application/vnd.api+json"},
    )

    assert response.status_code == 201
