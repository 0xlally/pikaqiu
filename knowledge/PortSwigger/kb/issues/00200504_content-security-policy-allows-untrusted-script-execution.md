# Content security policy: allows untrusted script execution

Source: https://portswigger.net/kb/issues/00200504_content-security-policy-allows-untrusted-script-execution
Fetched: 2026-06-28T09:17:09.524334+00:00

Support Center

Issue Definitions

Content security policy: allows untrusted script execution

Content security policy: allows untrusted script execution

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Content security policy: allows untrusted script execution

Content Security Policy (CSP) is a security mechanism designed to mitigate cross-site scripting attacks by disabling dangerous behaviours such as untrusted JavaScript execution. Websites can specify their security policy in a response header or meta tag, enabling fine-grained control over dangerous features like scripts and stylesheets.

Remediation: Content security policy: allows untrusted script execution

Mitigate cross-site scripting by avoiding 'unsafe-inline', 'unsafe-eval', data: URLs, and global wildcards in script directives. Use a secure, random nonce of at least 8 characters 'nonce-RANDOM' to prevent untrusted JavaScript execution.

References

Web Security Academy: What is CSP?

Web Security Academy: What is XSS?

Web Security Academy: Mitigating XSS attacks using CSP

Web Security Academy: Preventing XSS

Content Security Policy (CSP)

Vulnerability classifications

CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

CWE-80: Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-588: DOM-Based XSS

Typical severity

Information

Type index (hex)

0x00200504

Type index (decimal)

2098436

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
