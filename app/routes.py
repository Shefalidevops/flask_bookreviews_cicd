from flask import Blueprint, request, jsonify
from app.models import BookReview

api_bp = Blueprint("api", __name__)

@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "book-reviews-api"}), 200

@api_bp.route("/reviews", methods=["GET"])
def get_reviews():
    reviews = BookReview.get_all()
    return jsonify({"reviews": reviews, "count": len(reviews)}), 200

@api_bp.route("/reviews/<int:review_id>", methods=["GET"])
def get_review(review_id: int):
    review = BookReview.get_by_id(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review), 200

@api_bp.route("/reviews", methods=["POST"])
def create_review():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    required_fields = ["title", "author", "rating", "review_text"]
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    if not isinstance(data["rating"], int) or not (1 <= data["rating"] <= 5):
        return jsonify({"error": "Rating must be an integer between 1 and 5"}), 400
    
    review = BookReview.create(
        title=data["title"],
        author=data["author"],
        rating=data["rating"],
        review_text=data["review_text"]
    )
    
    return jsonify(review), 201

@api_bp.route("/reviews/<int:review_id>", methods=["PUT"])
def update_review(review_id: int):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if "rating" in data:
        if not isinstance(data["rating"], int) or not (1 <= data["rating"] <= 5):
            return jsonify({"error": "Rating must be an integer between 1 and 5"}), 400
    
    review = BookReview.update(
        review_id,
        title=data.get("title"),
        author=data.get("author"),
        rating=data.get("rating"),
        review_text=data.get("review_text")
    )
    
    if not review:
        return jsonify({"error": "Review not found"}), 404
    
    return jsonify(review), 200

@api_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id: int):
    success = BookReview.delete(review_id)
    
    if not success:
        return jsonify({"error": "Review not found"}), 404
    
    return jsonify({"message": "Review deleted successfully"}), 200
