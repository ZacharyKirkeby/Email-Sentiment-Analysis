from pyswip import Prolog

def analyze(subject, body, sentiment_score):

    """
    Sends the email subject, body, and sentiment score to Prolog for analysis.
    Prolog determines the category based on its rules.
    """
    print(subject)
    print(body)
    print(sentiment_score)

    prolog = Prolog()
    prolog.consult("sentiments.pl")
    prolog.assertz(f"email_subject('{subject}')")
    prolog.assertz(f"email_body('{body}')")
    prolog.assertz(f"sentiment_score(email, {sentiment_score})")
    result = list(prolog.query("email_category(email, Category)"))

    prolog.retractall("email_subject(_)")  
    prolog.retractall("email_body(_)")
    prolog.retractall("sentiment_score(_, _)")

    if result:
        return result[0]["Category"]
    else:
        return "uncategorized" 
