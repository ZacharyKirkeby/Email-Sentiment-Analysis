from textblob import TextBlob

def analyze_sentiment(email_body: str) -> float:

    """
    Analyzes the sentiment of the given email body.

    Args:
        email_body (str): The body of the email to analyze.

    Returns:
        float: A sentiment polarity score ranging from -1.0 (negative) 
               to 1.0 (positive). Neutral content returns a score near 0.
    """

    if not email_body.strip():
        # Return neutral for empty
        return 0.0

    blob = TextBlob(email_body)
    return blob.sentiment.polarity