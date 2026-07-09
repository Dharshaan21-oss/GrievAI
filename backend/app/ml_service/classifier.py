from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# Path to the extracted model folder (relative to project root)
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "ml_pipeline", "models", "grievai_distilbert_final"
)
MODEL_PATH = os.path.abspath(MODEL_PATH)

_tokenizer = None
_model = None

def load_classifier():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        _model.eval()
    return _tokenizer, _model

def classify_grievance(text: str):
    tokenizer, model = load_classifier()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]
        pred_id = int(torch.argmax(probs))
        confidence = float(probs[pred_id])
        category = model.config.id2label[pred_id]
    return {
        "category": category,
        "confidence": round(confidence, 4)
    }