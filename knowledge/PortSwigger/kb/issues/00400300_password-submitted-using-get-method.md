# Password submitted using GET method

Source: https://portswigger.net/kb/issues/00400300_password-submitted-using-get-method
Fetched: 2026-06-28T09:17:11.589681+00:00

Support Center

Issue Definitions

Password submitted using GET method

Password submitted using GET method

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Password submitted using GET method

Some applications use the GET method to submit passwords, which are transmitted within the query string of the requested URL. Sensitive information within URLs may be logged in various locations, including the user's browser, the web server, and any forward or reverse proxy servers between the two endpoints. URLs may also be displayed on-screen, bookmarked or emailed around by users. They may be disclosed to third parties via the Referer header when any off-site links are followed. Placing passwords into the URL increases the risk that they will be captured by an attacker.

Vulnerabilities that result in the disclosure of users' passwords can result in compromises that are extremely difficult to investigate due to obscured audit trails. Even if the application itself only handles non-sensitive information, exposing passwords puts users who have re-used their password elsewhere at risk.

Remediation: Password submitted using GET method

All forms submitting passwords should use the POST method. To achieve this, applications should specify the method attribute of the FORM tag as method="POST". It may also be necessary to modify the corresponding server-side form handler to ensure that submitted passwords are properly retrieved from the message body, rather than the URL.

Vulnerability classifications

CWE-598: Information Exposure Through Query Strings in GET Request

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Low

Type index (hex)

0x00400300

Type index (decimal)

4195072

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
