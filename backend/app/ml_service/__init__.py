from app.ml_service.classifier import classify_grievance
from app.ml_service.priority import compute_priority
from app.ml_service.duplicate_detector import add_to_index, find_duplicates
from app.ml_service.summarizer import summarize_grievance


def process_new_grievance(text: str, grievance_id: int = None):
    """
    Runs the full AI pipeline on a newly submitted grievance:
    1. Classify into a department category
    2. Score priority/urgency
    3. Check for duplicates against existing grievances
    4. Summarize (if long enough)

    Note: add_to_index() should be called separately AFTER the grievance is
    saved to the DB and has a real ID (see Step below on ordering).
    """
    classification = classify_grievance(text)
    priority = compute_priority(text)
    duplicates = find_duplicates(text) if grievance_id is None else find_duplicates(text)
    summary = summarize_grievance(text)

    return {
        "category": classification["category"],
        "category_confidence": classification["confidence"],
        "priority": priority["priority"],
        "priority_score": priority["combined_score"],
        "is_duplicate": len(duplicates) > 0,
        "duplicate_of_id": duplicates[0]["grievance_id"] if duplicates else None,
        "duplicate_matches": duplicates,
        "ai_summary": summary,
    }