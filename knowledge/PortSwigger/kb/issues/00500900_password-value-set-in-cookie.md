# Password value set in cookie

Source: https://portswigger.net/kb/issues/00500900_password-value-set-in-cookie
Fetched: 2026-06-28T09:17:13.485342+00:00

Support Center

Issue Definitions

Password value set in cookie

Password value set in cookie

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Password value set in cookie

Some applications issue a cookie containing the clear-text value of the password supplied by the user. This behavior increases the risk that users' passwords will be captured by an attacker. Any cookie-stealing vulnerabilities within the application or browser would enable an attacker to steal the user's credentials to the application.

Vulnerabilities that result in the disclosure of users' passwords can result in compromises that are extremely difficult to investigate due to obscured audit trails. Even if the application itself only handles non-sensitive information, exposing passwords puts users who have re-used their password elsewhere at risk.

Remediation: Password value set in cookie

Applications should not store user credentials within any client-side mechanism such as cookies.

Vulnerability classifications

CWE-287: Improper Authentication

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Medium

Type index (hex)

0x00500900

Type index (decimal)

5245184

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
