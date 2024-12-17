from transformers import pipeline

def summarize_and_tag(text):
    """
    Generate summaries and tags using NLP models.
    """
    summarizer = pipeline("summarization")
    keywords = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
    print(f"Summary: {summary}")

    return summary
