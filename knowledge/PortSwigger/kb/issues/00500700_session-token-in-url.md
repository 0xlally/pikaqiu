# Session token in URL

Source: https://portswigger.net/kb/issues/00500700_session-token-in-url
Fetched: 2026-06-28T09:17:13.010297+00:00

Support Center

Issue Definitions

Session token in URL

Session token in URL

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Session token in URL

Sensitive information within URLs may be logged in various locations, including the user's browser, the web server, and any forward or reverse proxy servers between the two endpoints. URLs may also be displayed on-screen, bookmarked or emailed around by users. They may be disclosed to third parties via the Referer header when any off-site links are followed. Placing session tokens into the URL increases the risk that they will be captured by an attacker.

Remediation: Session token in URL

Applications should use an alternative mechanism for transmitting session tokens, such as HTTP cookies or hidden fields in forms that are submitted using the POST method.

Vulnerability classifications

CWE-200: Information Exposure

CWE-384: Session Fixation

CWE-598: Information Exposure Through Query Strings in GET Request

CAPEC-593: Session Hijacking

Typical severity

Medium

Type index (hex)

0x00500700

Type index (decimal)

5244672

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
