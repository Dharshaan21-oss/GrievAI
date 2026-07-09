from transformers import pipeline

_sentiment_pipeline = None

# Keywords that indicate higher real-world urgency/severity regardless of tone
CRITICAL_KEYWORDS = [
    "fire", "collapsed", "collapse", "dead body", "electrocut", "accident",
    "death", "dying", "child", "children", "hospital emergency", "gas leak",
    "explosion", "drowning", "attack", "assault", "life threatening",
    "sparking", "live wire", "burst", "flooding", "flood"
]

HIGH_KEYWORDS = [
    "urgent", "immediately", "danger", "dangerous", "unsafe", "risk",
    "bribe", "corruption", "no water", "no electricity", "outbreak",
    "contaminated", "sewage", "leak", "broken", "damaged"
]

def load_sentiment_model():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            top_k=None
        )
    return _sentiment_pipeline

def keyword_severity_score(text: str) -> float:
    text_lower = text.lower()
    score = 0.0
    for kw in CRITICAL_KEYWORDS:
        if kw in text_lower:
            score += 0.4
    for kw in HIGH_KEYWORDS:
        if kw in text_lower:
            score += 0.15
    return min(score, 1.0)

def sentiment_score(text: str) -> float:
    """Returns a 0-1 'negativity intensity' score. Higher = more negative/distressed."""
    sentiment_pipe = load_sentiment_model()
    results = sentiment_pipe(text[:512])[0]  # list of {label, score}
    neg_score = 0.0
    for r in results:
        if r["label"].lower() in ("negative", "neg"):
            neg_score = r["score"]
    return neg_score

def compute_priority(text: str):
    kw_score = keyword_severity_score(text)
    sent_score = sentiment_score(text)

    # Weighted combination: keyword severity matters more (explicit danger signals)
    combined = (0.65 * kw_score) + (0.35 * sent_score)

    if combined >= 0.65:
        level = "critical"
    elif combined >= 0.4:
        level = "high"
    elif combined >= 0.2:
        level = "medium"
    else:
        level = "low"

    return {
        "priority": level,
        "combined_score": round(combined, 3),
        "keyword_score": round(kw_score, 3),
        "sentiment_score": round(sent_score, 3),
    }