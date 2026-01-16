from typing import Dict, List, Optional
from datetime import datetime


class BookReview:
    reviews: Dict[int, Dict] = {}
    next_id: int = 1

    @classmethod
    def create(cls, title: str, author: str, rating: int, review_text: str) -> Dict:
        review = {
            "id": cls.next_id,
            "title": title,
            "author": author,
            "rating": rating,
            "review_text": review_text,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        cls.reviews[cls.next_id] = review
        cls.next_id += 1
        return review

    @classmethod
    def get_all(cls) -> List[Dict]:
        return list(cls.reviews.values())

    @classmethod
    def get_by_id(cls, review_id: int) -> Optional[Dict]:
        return cls.reviews.get(review_id)

    @classmethod
    def update(
        cls,
        review_id: int,
        title: Optional[str] = None,
        author: Optional[str] = None,
        rating: Optional[int] = None,
        review_text: Optional[str] = None,
    ) -> Optional[Dict]:
        review = cls.reviews.get(review_id)
        if not review:
            return None

        if title is not None:
            review["title"] = title
        if author is not None:
            review["author"] = author
        if rating is not None:
            review["rating"] = rating
        if review_text is not None:
            review["review_text"] = review_text

        review["updated_at"] = datetime.utcnow().isoformat()
        return review

    @classmethod
    def delete(cls, review_id: int) -> bool:
        if review_id in cls.reviews:
            del cls.reviews[review_id]
            return True
        return False

    @classmethod
    def clear_all(cls) -> None:
        cls.reviews.clear()
        cls.next_id = 1
