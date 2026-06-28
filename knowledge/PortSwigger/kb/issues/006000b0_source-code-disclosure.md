# Source code disclosure

Source: https://portswigger.net/kb/issues/006000b0_source-code-disclosure
Fetched: 2026-06-28T09:17:16.995725+00:00

Support Center

Issue Definitions

Source code disclosure

Source code disclosure

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Source code disclosure

Source code intended to be kept server-side can sometimes end up being disclosed to users. Such code may contain sensitive information such as database passwords and secret keys, which may help malicious users formulate attacks against the application.

Remediation: Source code disclosure

Server-side source code is normally disclosed to clients as a result of typographical errors in scripts or because of misconfiguration, such as failing to grant executable permissions to a script or directory. Review the cause of the code disclosure and prevent it from happening.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-18: Source Code

CWE-200: Information Exposure

CWE-388: Error Handling

CWE-540: Information Exposure Through Source Code

CWE-541: Information Exposure Through Include Source Code

CWE-615: Information Exposure Through Comments

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Low

Type index (hex)

0x006000b0

Type index (decimal)

6291632

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
