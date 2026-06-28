# Content security policy: allows clickjacking

Source: https://portswigger.net/kb/issues/00200507_content-security-policy-allows-clickjacking
Fetched: 2026-06-28T09:17:09.228361+00:00

Support Center

Issue Definitions

Content security policy: allows clickjacking

Content security policy: allows clickjacking

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Content security policy: allows clickjacking

Content Security Policy (CSP) is a security mechanism designed to mitigate cross-site scripting attacks by disabling dangerous behaviours such as untrusted JavaScript execution. Websites can specify their security policy in a response header or meta tag, enabling fine-grained control over dangerous features like scripts and stylesheets.

Remediation: Content security policy: allows clickjacking

We recommend that you set the frame-ancestors directive to 'none' if you do not want your site to be framed, or 'self' if you want to allow it to frame itself. In addition, use the X-Frame-Options header with DENY or SAMEORIGIN, based on your needs.

References

Web Security Academy: Clickjacking

X-Frame-Options

Web Security Academy: What is CSP?

Web Security Academy: Protecting against clickjacking using CSP

Content Security Policy (CSP)

Vulnerability classifications

CWE-693: Protection Mechanism Failure

CWE-1021: Improper Restriction of Rendered UI Layers or Frames

CAPEC-103: Clickjacking

Typical severity

Information

Type index (hex)

0x00200507

Type index (decimal)

2098439

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
