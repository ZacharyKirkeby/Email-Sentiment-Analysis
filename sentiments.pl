% Facts: Keywords and their corresponding categories

% Spam Keywords
keyword_category("offer", spam).
keyword_category("limited time", spam).
keyword_category("act now", spam).
keyword_category("gold", spam).
keyword_category("silver", spam).
keyword_category("MAGA", spam).
keyword_category("patriot", spam).
keyword_category("win big", spam).
keyword_category("urgent", spam).
keyword_category("risk-free", spam).
keyword_category("free money", spam).
keyword_category("limited offer", spam).
keyword_category("click here", spam).
keyword_category("100% guaranteed", spam).
keyword_category("apply now", spam).
keyword_category("exclusive deal", spam).
keyword_category("cash bonus", spam).
keyword_category("vip offer", spam).
keyword_category("gift card", spam).
keyword_category("get rich quick", spam).
keyword_category("no strings attached", spam).
keyword_category("investment opportunity", spam).
keyword_category("lottery winner", spam).
keyword_category("claim prize", spam).
keyword_category("act fast", spam).
keyword_category("credit card offer", spam).
keyword_category("special deal", spam).
keyword_category("free quote", spam).
keyword_category("last chance", spam).
keyword_category("double your income", spam).
keyword_category("your account is at risk", spam).
keyword_category("account suspension", spam).
keyword_category("unauthorized login", spam).
keyword_category("password reset", spam).
keyword_category("verify account", spam).
keyword_category("phishing alert", spam).
keyword_category("fraud detected", spam).
keyword_category("item shared", spam).
keyword_category("suspicious activity", spam).
keyword_category("failed delivery", spam).
keyword_category("exotic", spam).
keyword_category("sexy", spam).
keyword_category("hookup", spam).
keyword_category("love", spam).

% Marketing Keywords
% TBH half of these are basically spam
keyword_category("new product", marketing).
keyword_category("best seller", marketing).
keyword_category("special promotion", marketing).
keyword_category("holiday sale", marketing).
keyword_category("flash sale", marketing).
keyword_category("end-of-season", marketing).
keyword_category("buy one get one", marketing).
keyword_category("exclusive access", marketing).
keyword_category("deal of the day", marketing).
keyword_category("shop now", marketing).
keyword_category("limited stock", marketing).
keyword_category("save big", marketing).
keyword_category("sale", marketing).
keyword_category("discount", marketing).
keyword_category("free trial", marketing).
keyword_category("bundle offer", marketing).
keyword_category("extra savings", marketing).
keyword_category("membership discount", marketing).
keyword_category("reward points", marketing).
keyword_category("holiday discounts", marketing).
keyword_category("early access", marketing).
keyword_category("coupon code", marketing).
keyword_category("new arrivals", marketing).
keyword_category("back-to-school", marketing).
keyword_category("cyber monday", marketing).

% Informative Keywords
keyword_category("monthly report", informative).
keyword_category("weekly summary", informative).
keyword_category("project update", informative).
keyword_category("meeting minutes", informative).
keyword_category("year-end review", informative).
keyword_category("budget planning", informative).
keyword_category("financial statement", informative).
keyword_category("team goals", informative).
keyword_category("industry insights", informative).
keyword_category("training schedule", informative).
keyword_category("workshop details", informative).
keyword_category("client feedback", informative).
keyword_category("audit results", informative).
keyword_category("policy changes", informative).
keyword_category("compliance notice", informative).
keyword_category("system update", informative).
keyword_category("important changes", informative).
keyword_category("technical update", informative).
keyword_category("performance metrics", informative).
keyword_category("revised guidelines", informative).
keyword_category("security notice", informative).
keyword_category("support contact", informative).
keyword_category("best practices", informative).
keyword_category("case study", informative).
keyword_category("research findings", informative).
keyword_category("summary", informative).
keyword_category("report", informative).

% Neutral or General Keywords
keyword_category("thank you", neutral).
keyword_category("follow-up", neutral).
keyword_category("response required", neutral).
keyword_category("feedback request", neutral).
keyword_category("appointment reminder", neutral).
keyword_category("invitation", neutral).
keyword_category("reminder", neutral).
keyword_category("customer support", neutral).
keyword_category("your order", neutral).
keyword_category("tracking number", neutral).
keyword_category("return policy", neutral).
keyword_category("delivery details", neutral).
keyword_category("payment confirmation", neutral).
keyword_category("account balance", neutral).
keyword_category("new message", neutral).
keyword_category("unsubscribe", neutral).
keyword_category("email preferences", neutral).
keyword_category("system notification", neutral).
keyword_category("technical support", neutral).
keyword_category("billing inquiry", neutral).
keyword_category("schedule update", neutral).
keyword_category("travel itinerary", neutral).
keyword_category("reservation confirmation", neutral).
keyword_category("event details", neutral).
keyword_category("calendar invite", neutral).


% Rule: Categorize email based on both keyword occurrence and sentiment analysis.

email_category(Email, spam) :-
    contains_keyword(Email, Keyword),
    keyword_category(Keyword, spam),
    sentiment_category(Email, positive),
    keyword_frequency(Email, Keyword, Frequency),
    Frequency > 1. % Emails with multiple mentions of spam-related keywords have a higher spam likelihood.

email_category(Email, marketing) :-
    contains_keyword(Email, Keyword),
    keyword_category(Keyword, marketing),
    sentiment_category(Email, positive),
    keyword_frequency(Email, Keyword, Frequency),
    Frequency > 1. % Multiple marketing keywords increase the likelihood of being categorized as marketing.

email_category(Email, informative) :-
    contains_keyword(Email, Keyword),
    keyword_category(Keyword, informative),
    sentiment_category(Email, neutral).

email_category(Email, mixed) :- 
    contains_keyword(Email, Keyword),
    (keyword_category(Keyword, spam); keyword_category(Keyword, marketing)),
    sentiment_category(Email, neutral).

% Rule mixed category
% marketing or spam keywords appear with a neutral sentiment -> prob spam tbh

email_category(Email, mixed) :-
    contains_keyword(Email, Keyword),
    (keyword_category(Keyword, spam); keyword_category(Keyword, marketing)),
    sentiment_category(Email, neutral).

% Rule  categorizing based on subject and body

email_category(Email, spam) :-
    (contains_keyword(Email, Keyword), keyword_category(Keyword, spam); contains_subject(Email, Keyword), keyword_category(Keyword, spam)),
    sentiment_category(Email, positive).

email_category(Email, marketing) :-
    (contains_keyword(Email, Keyword), keyword_category(Keyword, marketing); contains_subject(Email, Keyword), keyword_category(Keyword, marketing)),
    sentiment_category(Email, positive).

sentiment_category(Email, positive) :-
    sentiment_score(Email, Score),
    Score > 0.4, 
    \+ contains_negation(Email).

sentiment_category(Email, neutral) :-
    sentiment_score(Email, Score),
    Score =< 0.4, 
    Score >= -0.4.

sentiment_category(Email, negative) :-
    sentiment_score(Email, Score),
    Score < -0.4.

% Sentiment with negation detection (no urgency)
contains_negation(Email) :-
    (contains_keyword(Email, "not"); contains_keyword(Email, "no")),
    contains_keyword(Email, "urgent").

% Rule for keyword frequency 
keyword_frequency(Email, Keyword, Frequency) :-
    findall(Keyword, contains_keyword(Email, Keyword), Keywords),
    length(Keywords, Frequency).

% Rule WIP - sender quality

email_category(Email, spam) :-
    sender_address(Email, Address),
    (sub_string(Address, _, _, _, "offer"); sub_string(Address, _, _, _, "support")),
    sentiment_category(Email, positive).

% Rules for subject and body matching

contains_subject(Email, Keyword) :-
    email_subject(Email, Subject),
    sub_string(Subject, _, _, _, Keyword).

contains_body(Email, Keyword) :-
    email_body(Email, Body),
    sub_string(Body, _, _, _, Keyword).
