from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

_tokenizer = None
_model = None

def load_summarizer():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        _model.eval()
    return _tokenizer, _model

def summarize_grievance(text: str, max_length: int = 60, min_length: int = 15) -> str:
    """
    Summarizes grievance text. Skips summarization for already-short text
    (summarizing a 1-sentence complaint often produces nonsense or just repeats it).
    """
    word_count = len(text.split())
    if word_count <= 25:
        return text.strip()

    tokenizer, model = load_summarizer()
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=1024
    )
    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            min_length=min_length,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True,
        )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary.strip()