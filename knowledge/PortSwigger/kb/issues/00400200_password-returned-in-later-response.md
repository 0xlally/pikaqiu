# Password returned in later response

Source: https://portswigger.net/kb/issues/00400200_password-returned-in-later-response
Fetched: 2026-06-28T09:17:11.373776+00:00

Support Center

Issue Definitions

Password returned in later response

Password returned in later response

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Password returned in later response

Some applications return passwords submitted to the application in clear form in later responses. This behavior increases the risk that users' passwords will be captured by an attacker. Many types of vulnerability, such as weaknesses in session handling, broken access controls, and cross-site scripting, could enable an attacker to leverage this behavior to retrieve the passwords of other application users. This possibility typically exacerbates the impact of those other vulnerabilities, and in some situations can enable an attacker to quickly compromise the entire application.

Vulnerabilities that result in the disclosure of users' passwords can result in compromises that are extremely difficult to investigate due to obscured audit trails. Even if the application itself only handles non-sensitive information, exposing passwords puts users who have re-used their password elsewhere at risk.

Remediation: Password returned in later response

There is usually no good reason for an application to return users' passwords in its responses. If user impersonation is a business requirement this would be better implemented as a custom function with associated logging.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-204: Response Discrepancy Information Exposure

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Medium

Type index (hex)

0x00400200

Type index (decimal)

4194816

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
