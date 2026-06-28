# Content security policy: allows form hijacking

Source: https://portswigger.net/kb/issues/00200508_content-security-policy-allows-form-hijacking
Fetched: 2026-06-28T09:17:09.284245+00:00

Support Center

Issue Definitions

Content security policy: allows form hijacking

Content security policy: allows form hijacking

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Content security policy: allows form hijacking

Content Security Policy (CSP) is a security mechanism designed to mitigate cross-site scripting attacks by disabling dangerous behaviours such as untrusted JavaScript execution. Websites can specify their security policy in a response header or meta tag, enabling fine-grained control over dangerous features like scripts and stylesheets.

Remediation: Content security policy: allows form hijacking

We recommend using the form-action directive in the CSP response header to control form post destinations. If no form actions are used, set form-action to 'none' to block untrusted forms. For applications without external form URLs, use 'self' to allow only same-origin URLs. If needed, allow list hosts for external URL form submissions, but be aware this lets attackers submit to these external resources.

References

PortSwigger Research: Stealing passwords from infosec Mastodon - without bypassing CSP

Web Security Academy: What is CSP?

Content Security Policy (CSP)

Vulnerability classifications

CWE-116: Improper Encoding or Escaping of Output

Typical severity

Information

Type index (hex)

0x00200508

Type index (decimal)

2098440

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
