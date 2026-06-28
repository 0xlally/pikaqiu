# CSS injection (reflected)

Source: https://portswigger.net/kb/issues/00501300_css-injection-reflected
Fetched: 2026-06-28T09:17:16.066518+00:00

Support Center

Issue Definitions

CSS injection (reflected)

CSS injection (reflected)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: CSS injection (reflected)

CSS injection vulnerabilities arise when an application imports a style sheet from a user-supplied URL, or embeds user input in CSS blocks without adequate escaping. They are closely related to cross-site scripting (XSS) vulnerabilities but often trickier to exploit.

Being able to inject arbitrary CSS into the victim's browser may enable various attacks, including:

Executing arbitrary JavaScript using IE's expression() function.

Using CSS selectors to read parts of the HTML source, which may include sensitive data such as anti-CSRF tokens.

Capturing any sensitive data within the URL query string by making a further style sheet import to a URL on the attacker's domain, and monitoring the incoming Referer header.

Remediation: CSS injection (reflected)

Ensure that user input is adequately escaped before embedding it in CSS blocks, and consider using a whitelist to prevent loading of arbitrary style sheets.

References

Malicious CSS

Abusing unicode-range of @font-face

Vulnerability classifications

CWE-73: External Control of File Name or Path

CWE-20: Improper Input Validation

CAPEC-468: Generic Cross-Browser Cross-Domain Theft

Typical severity

Medium

Type index (hex)

0x00501300

Type index (decimal)

5247744

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
