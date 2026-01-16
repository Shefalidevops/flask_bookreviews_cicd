import pytest
from app.models import BookReview


@pytest.fixture(autouse=True)
def reset_reviews():
    BookReview.clear_all()
    yield
    BookReview.clear_all()


def test_create_review():
    review = BookReview.create(
        title="1984",
        author="George Orwell",
        rating=5,
        review_text="A dystopian masterpiece",
    )

    assert review["id"] == 1
    assert review["title"] == "1984"
    assert review["author"] == "George Orwell"
    assert review["rating"] == 5
    assert "created_at" in review


def test_get_all_reviews():
    BookReview.create("Book 1", "Author 1", 4, "Good read")
    BookReview.create("Book 2", "Author 2", 5, "Excellent")

    reviews = BookReview.get_all()
    assert len(reviews) == 2


def test_get_by_id():
    review = BookReview.create("Test Book", "Test Author", 3, "Average")
    retrieved = BookReview.get_by_id(review["id"])

    assert retrieved is not None
    assert retrieved["title"] == "Test Book"


def test_get_nonexistent_review():
    result = BookReview.get_by_id(999)
    assert result is None


def test_update_review():
    review = BookReview.create("Original", "Author", 3, "Text")
    updated = BookReview.update(review["id"], title="Updated Title", rating=5)

    assert updated["title"] == "Updated Title"
    assert updated["rating"] == 5
    assert updated["author"] == "Author"


def test_delete_review():
    review = BookReview.create("Delete Me", "Author", 2, "Text")
    success = BookReview.delete(review["id"])

    assert success is True
    assert BookReview.get_by_id(review["id"]) is None


def test_delete_nonexistent():
    success = BookReview.delete(999)
    assert success is False
