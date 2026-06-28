# Content security policy: allows untrusted style execution

Source: https://portswigger.net/kb/issues/00200505_content-security-policy-allows-untrusted-style-execution
Fetched: 2026-06-28T09:17:09.091290+00:00

Support Center

Issue Definitions

Content security policy: allows untrusted style execution

Content security policy: allows untrusted style execution

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Content security policy: allows untrusted style execution

Content Security Policy (CSP) is a security mechanism designed to mitigate cross-site scripting attacks by disabling dangerous behaviours such as untrusted JavaScript execution. Websites can specify their security policy in a response header or meta tag, enabling fine-grained control over dangerous features like scripts and stylesheets.

Remediation: Content security policy: allows untrusted style execution

Mitigate style-based data exfiltration by avoiding 'unsafe-inline', data: URLs, and global wildcards in style directives. Use a secure, random nonce of at least 8 characters 'nonce-RANDOM' in the relevant directive.

References

Web Security Academy: What is CSP?

PortSwigger Research: Blind CSS exfiltration

PortSwigger Research: Offensive CSS research

Content Security Policy (CSP)

Vulnerability classifications

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-468: Generic Cross-Browser Cross-Domain Theft

Typical severity

Information

Type index (hex)

0x00200505

Type index (decimal)

2098437

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
