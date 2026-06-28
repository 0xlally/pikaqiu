# Password returned in URL query string

Source: https://portswigger.net/kb/issues/00400400_password-returned-in-url-query-string
Fetched: 2026-06-28T09:17:11.652957+00:00

Support Center

Issue Definitions

Password returned in URL query string

Password returned in URL query string

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Password returned in URL query string

The application responds to login submissions with a link containing the user's password within the URL query string. Sensitive information within URLs may be logged in various locations, including the user's browser, the web server, and any forward or reverse proxy servers between the two endpoints. URLs may also be displayed on-screen, bookmarked or emailed around by users. They may be disclosed to third parties via the Referer header when any off-site links are followed. Placing passwords into the URL increases the risk that they will be captured by an attacker.

Vulnerabilities that result in the disclosure of users' passwords can result in compromises that are extremely difficult to investigate due to obscured audit trails. Even if the application itself only handles non-sensitive information, exposing passwords puts users who have re-used their password elsewhere at risk.

Remediation: Password returned in URL query string

The application should never transmit any sensitive information within the URL query string. There is no good reason for a login mechanism to echo passwords back to the user, and the mechanism should be modified to remove this behavior.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-598: Information Exposure Through Query Strings in GET Request

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Low

Type index (hex)

0x00400400

Type index (decimal)

4195328

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
