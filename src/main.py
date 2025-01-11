from email_ingestion import fetch_emails
from extract_query import analyze
from sentiment import analyze_sentiment
#from visualizer import generate_reports


# TBH this file is kinda pointless but I wanted to be a tad more organized than usual because I tend to make
# some really messy files. 


# TODO - user input for num emails to fetch\

def main():
    fetch_count = 5
    emails = fetch_emails(fetch_count)
    results = []
    count = 0
    
    # test running without pipeline rn

    # the pipeline
    for email_id, email_content in emails.items():
        if count == 5:
            break
        sentiment_score = analyze_sentiment(email_content) 
        category = analyze(email_id, email_content, sentiment_score)
        results.append({"email_id": email_id, "category": category})
        count += 1
    print(results)

    # shiny pretty pictures 
    #generate_reports(results)

if __name__ == "__main__":
    main()

