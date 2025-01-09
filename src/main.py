from email_ingestion import fetch_emails
from extract_query import analyze
from sentiment import analyze_sentiment
from visualizer import generate_reports


# TBH this file is kinda pointless but I wanted to be a tad more organized than usual because I tend to make
# some really messy files. 

def main():
    emails = fetch_emails()
    results = []

    # the pipeline
    for email_id, email_content in emails.items():
        sentiment_score = analyze_sentiment(email_content) 
        category = analyze(email_id, email_content, sentiment_score)
        results.append({"email_id": email_id, "category": category})

    # shiny pretty pictures 
    generate_reports(results)

if __name__ == "__main__":
    main()

