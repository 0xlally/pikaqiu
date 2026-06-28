# Client-side HTTP parameter pollution (reflected)

Source: https://portswigger.net/kb/issues/00501400_client-side-http-parameter-pollution-reflected
Fetched: 2026-06-28T09:17:15.922023+00:00

Support Center

Issue Definitions

Client-side HTTP parameter pollution (reflected)

Client-side HTTP parameter pollution (reflected)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Client-side HTTP parameter pollution (reflected)

Client-side HTTP parameter pollution (HPP) vulnerabilities arise when an application embeds user input in URLs in an unsafe manner. An attacker can use this vulnerability to construct a URL that, if visited by another application user, will modify URLs within the response by inserting additional query string parameters and sometimes overriding existing ones. This may result in links and forms having unexpected side effects. For example, it may be possible to modify an invitation form using HPP so that the invitation is delivered to an unexpected recipient.

The security impact of this issue depends largely on the nature of the application functionality. Even if it has no direct impact on its own, an attacker may use it in conjunction with other vulnerabilities to escalate their overall severity.

Remediation: Client-side HTTP parameter pollution (reflected)

Ensure that user input is URL-encoded before it is embedded in a URL.

References

HTTP Parameter Pollution

Vulnerability classifications

CWE-233: Improper Handling of Parameters

CWE-20: Improper Input Validation

CAPEC-460: HTTP Parameter Pollution (HPP)

Typical severity

Low

Type index (hex)

0x00501400

Type index (decimal)

5248000

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
