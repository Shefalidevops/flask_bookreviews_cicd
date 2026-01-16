import pytest
from app import create_app
from app.models import BookReview


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    BookReview.clear_all()


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_empty_reviews(client):
    response = client.get("/api/v1/reviews")
    assert response.status_code == 200
    assert response.json["count"] == 0


def test_create_review(client):
    data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "rating": 5,
        "review_text": "A classic American novel",
    }

    response = client.post("/api/v1/reviews", json=data)
    assert response.status_code == 201
    assert response.json["title"] == "The Great Gatsby"
    assert response.json["id"] == 1


def test_create_review_missing_fields(client):
    data = {"title": "Incomplete"}

    response = client.post("/api/v1/reviews", json=data)
    assert response.status_code == 400
    assert "Missing required fields" in response.json["error"]


def test_create_review_invalid_rating(client):
    data = {"title": "Test", "author": "Author", "rating": 6, "review_text": "Text"}

    response = client.post("/api/v1/reviews", json=data)
    assert response.status_code == 400


def test_get_review_by_id(client):
    data = {
        "title": "Test Book",
        "author": "Test Author",
        "rating": 4,
        "review_text": "Good",
    }

    create_response = client.post("/api/v1/reviews", json=data)
    review_id = create_response.json["id"]

    response = client.get(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json["title"] == "Test Book"


def test_get_nonexistent_review(client):
    response = client.get("/api/v1/reviews/999")
    assert response.status_code == 404


def test_update_review(client):
    data = {"title": "Original", "author": "Author", "rating": 3, "review_text": "Okay"}

    create_response = client.post("/api/v1/reviews", json=data)
    review_id = create_response.json["id"]

    update_data = {"title": "Updated Title", "rating": 5}
    response = client.put(f"/api/v1/reviews/{review_id}", json=update_data)

    assert response.status_code == 200
    assert response.json["title"] == "Updated Title"
    assert response.json["rating"] == 5


def test_delete_review(client):
    data = {"title": "Delete", "author": "Author", "rating": 2, "review_text": "Text"}

    create_response = client.post("/api/v1/reviews", json=data)
    review_id = create_response.json["id"]

    response = client.delete(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200

    get_response = client.get(f"/api/v1/reviews/{review_id}")
    assert get_response.status_code == 404
