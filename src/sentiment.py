from textblob import TextBlob

def analyze_sentiment(email: dict | str) -> float:
    if isinstance(email, dict):
        # Extract the body if it's a dictionary
        email_body = email.get("body", "")
    elif isinstance(email, str):
        email_body = email
    else:
        # Raise an error if the input type is unsupported
        raise TypeError(f"Expected a string or dictionary, but got {type(email).__name__}")

    # Handle empty or invalid body
    if not isinstance(email_body, str) or not email_body.strip():
        return 0.0

    # Analyze sentiment
    blob = TextBlob(email_body)
    return blob.sentiment.polarity
